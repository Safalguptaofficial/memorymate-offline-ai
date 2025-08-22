# Vad_listener.py
import os
from transcribe_and_respond import transcribe_with_whisper, generate_llama_response
from tts import speak_text  # Your TTS system

AUDIO_FILE = "my_voice.wav"


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
