# Vad_listener.py
import os
from transcribe_and_respond import transcribe_with_whisper, generate_llama_response
from tts import speak_text  # Your TTS system
import webrtcvad
import sounddevice as sd
import numpy as np
import wave
import threading
import time
from collections import deque


AUDIO_FILE = "my_voice.wav"


class VoiceActivityDetector:
    def __init__(self, sample_rate=16000, frame_duration_ms=30, aggressiveness=2):
        self.sample_rate = sample_rate
        self.frame_duration_ms = frame_duration_ms
        self.aggressiveness = aggressiveness
        self.vad = webrtcvad.Vad(aggressiveness)
        self.frame_size = int(sample_rate * frame_duration_ms / 1000)
        self.is_recording = False
        self.audio_buffer = deque()
        self.silence_threshold = 0.5  # seconds of silence to stop recording
        self.last_voice_time = time.time()  # Instance variable
        
    def record_with_vad(self, filename="recording.wav", max_duration=30):
        """Record audio with voice activity detection"""
        print("🎤 Listening for voice activity...")
        print("💡 Speak now to start recording, stay silent to stop")
        
        self.is_recording = True
        self.audio_buffer.clear()
        self.last_voice_time = time.time()  # Reset voice time
        
        # Start recording in a separate thread
        recording_thread = threading.Thread(
            target=self._record_audio,
            args=(filename, max_duration)
        )
        recording_thread.start()
        
        # Wait for recording to complete
        recording_thread.join()
        
        print(f"✅ Recording saved as '{filename}'")
        return filename
    
    def _record_audio(self, filename, max_duration):
        """Internal recording function"""
        start_time = time.time()
        
        def audio_callback(indata, frames, callback_time, status):
            if status:
                print(f"Audio callback status: {status}")
            
            if not self.is_recording:
                return
            
            # Convert to 16-bit PCM
            audio_data = (indata[:, 0] * 32767).astype(np.int16)
            
            # Check for voice activity
            if self._detect_voice(audio_data):
                self.last_voice_time = time.time()
                self.audio_buffer.extend(audio_data)
            else:
                # Check if we've been silent for too long
                if time.time() - self.last_voice_time > self.silence_threshold:
                    if len(self.audio_buffer) > 0:
                        self.is_recording = False
                        return
            
            # Check max duration
            if time.time() - start_time > max_duration:
                self.is_recording = False
                return
        
        try:
            with sd.InputStream(
                callback=audio_callback,
                channels=1,
                samplerate=self.sample_rate,
                dtype=np.float32,
                blocksize=self.frame_size
            ):
                while self.is_recording:
                    time.sleep(0.1)
                    
        except Exception as e:
            print(f"Recording error: {e}")
            self.is_recording = False
        
        # Save the recorded audio
        if len(self.audio_buffer) > 0:
            self._save_audio(filename)
    
    def _detect_voice(self, audio_data):
        """Detect voice activity in audio frame"""
        try:
            # Convert to bytes for webrtcvad
            audio_bytes = audio_data.tobytes()
            
            # Check if frame size matches expected size
            if len(audio_bytes) == self.frame_size * 2:  # 16-bit = 2 bytes per sample
                return self.vad.is_speech(audio_bytes, self.sample_rate)
            else:
                # Pad or truncate to match frame size
                target_size = self.frame_size * 2
                if len(audio_bytes) < target_size:
                    audio_bytes = audio_bytes.ljust(target_size, b'\x00')
                else:
                    audio_bytes = audio_bytes[:target_size]
                
                return self.vad.is_speech(audio_bytes, self.sample_rate)
        except Exception as e:
            # Fallback: simple amplitude-based detection
            return np.mean(np.abs(audio_data)) > 0.01
    
    def _save_audio(self, filename):
        """Save recorded audio to WAV file"""
        if len(self.audio_buffer) == 0:
            return
        
        # Convert deque to numpy array
        audio_array = np.array(list(self.audio_buffer), dtype=np.int16)
        
        # Save as WAV file
        with wave.open(filename, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(audio_array.tobytes())
    
    def stop_recording(self):
        """Stop recording manually"""
        self.is_recording = False


def record_with_vad(filename="my_voice.wav", duration=10):
    """Simple function to record with VAD"""
    vad = VoiceActivityDetector()
    return vad.record_with_vad(filename, duration)


# Alternative simple recording function for when VAD is not available
def record_simple(filename="my_voice.wav", duration=5):
    """Simple recording without VAD"""
    fs = 16000
    print(f"🎤 Recording for {duration} seconds...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    
    # Save as WAV
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(fs)
        wav_file.writeframes((recording * 32767).astype(np.int16).tobytes())
    
    print(f"✅ Recording saved as '{filename}'")
    return filename


def main():
    print("🎙️ Welcome to MemoryMate v0.2 (Offline AI + TTS)")

    # Step 1: Record with VAD
    print("🎤 Listening... Start speaking to activate VAD.")
    record_with_vad(AUDIO_FILE)
    print(f"✅ Recording saved as '{AUDIO_FILE}'\n")

    # Step 2: Transcribe
    transcript = transcribe_with_whisper(AUDIO_FILE)
    print(f"📝 You said: {transcript}\n")

    # Step 3: Generate response from LLaMA
    response = generate_llama_response(transcript)
    print("🧠 LLaMA says:")
    print(response)

    # Step 4: Speak it out
    speak_text(response)


if __name__ == "__main__":
    main()
