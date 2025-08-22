import pyttsx3
import os
import platform


class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        self._configure_engine()
    
    def _configure_engine(self):
        """Configure TTS engine based on platform and preferences"""
        # Get available voices
        voices = self.engine.getProperty('voices')
        
        # Set voice (prefer female voice if available)
        if voices:
            # Try to find a female voice
            female_voice = None
            for voice in voices:
                if 'female' in voice.name.lower() or 'samantha' in voice.name.lower():
                    female_voice = voice.id
                    break
            
            if female_voice:
                self.engine.setProperty('voice', female_voice)
            else:
                self.engine.setProperty('voice', voices[0].id)
        
        # Set speech rate (words per minute)
        self.engine.setProperty('rate', 180)
        
        # Set volume (0.0 to 1.0)
        self.engine.setProperty('volume', 0.9)
    
    def speak(self, text: str, block: bool = True):
        """Speak the given text"""
        try:
            if block:
                self.engine.say(text)
                self.engine.runAndWait()
            else:
                self.engine.say(text)
                self.engine.startLoop(False)
        except Exception as e:
            print(f"TTS Error: {e}")
            # Fallback to system commands
            self._fallback_speak(text)
    
    def _fallback_speak(self, text: str):
        """Fallback TTS using system commands"""
        system = platform.system()
        try:
            if system == "Darwin":  # macOS
                os.system(f'say "{text}"')
            elif system == "Linux":
                os.system(f'espeak "{text}"')
            elif system == "Windows":
                os.system(f'powershell -Command "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{text}\')"')
        except Exception as e:
            print(f"Fallback TTS also failed: {e}")
    
    def stop(self):
        """Stop current speech"""
        try:
            self.engine.stop()
        except:
            pass
    
    def change_voice(self, voice_id: str):
        """Change to a specific voice"""
        try:
            self.engine.setProperty('voice', voice_id)
        except Exception as e:
            print(f"Could not change voice: {e}")
    
    def change_rate(self, rate: int):
        """Change speech rate (words per minute)"""
        self.engine.setProperty('rate', rate)
    
    def change_volume(self, volume: float):
        """Change volume (0.0 to 1.0)"""
        self.engine.setProperty('volume', max(0.0, min(1.0, volume)))


# Global TTS instance
tts_engine = TextToSpeech()


def speak_text(text: str, block: bool = True):
    """Global function to speak text"""
    tts_engine.speak(text, block)


def stop_speech():
    """Global function to stop speech"""
    tts_engine.stop()
