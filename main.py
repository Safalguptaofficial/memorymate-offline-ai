# main.py
import subprocess
import os
from record import record_voice
import pyttsx3  # NEW: For Text-to-Speech

# === Path Config ===
WHISPER_BIN = os.path.expanduser("~/whisper.cpp/build/bin/whisper-cli")
WHISPER_MODEL = os.path.expanduser("~/whisper.cpp/models/ggml-base.en.bin")
LLAMA_BIN = os.path.expanduser("~/llama.cpp/build/bin/llama-cli")
LLAMA_MODEL = os.path.expanduser(
    "~/llama.cpp/models/mistral-7b-instruct-v0.1.Q4_K_M.gguf")

AUDIO_FILE = "my_voice.wav"

# === NEW: Text-to-Speech Function ===


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# === Transcription ===


def transcribe(audio_path):
    print("\n🧠 Transcribing with Whisper.cpp...")
    cmd = [WHISPER_BIN, "-m", WHISPER_MODEL, "-f", audio_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ Whisper failed:", result.stderr)
        return ""

    lines = result.stdout.strip().split("\n")
    transcript = ""
    for line in reversed(lines):
        if "]" in line:
            transcript = line.split("]")[-1].strip()
            break
    print(f"📝 You said: {transcript}")
    return transcript

# === Query LLaMA ===


def query_llama(prompt):
    print("\n🤖 Asking LLaMA.cpp...")
    cmd = [LLAMA_BIN, "-m", LLAMA_MODEL, "-p", prompt, "--n-predict", "100"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ LLaMA failed:", result.stderr)
        return ""

    output = result.stdout.strip()
    print("\n🧠 LLaMA says:")
    print(output)
    return output


# === Main App ===
if __name__ == "__main__":
    print("🎙️ Welcome to MemoryMate v0.2 (Offline AI + TTS)")
    record_voice(filename=AUDIO_FILE, duration=5)
    user_text = transcribe(AUDIO_FILE)
    if user_text:
        response = query_llama(user_text)
        speak(response)  # NEW: Speak the response aloud
