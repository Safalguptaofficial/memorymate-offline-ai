import subprocess
import os
import json
from record import record_voice

# === Path Config ===
WHISPER_BIN = os.path.expanduser("~/whisper.cpp/build/bin/whisper-cli")
WHISPER_MODEL = os.path.expanduser("~/whisper.cpp/models/ggml-base.en.bin")
LLAMA_BIN = os.path.expanduser("~/llama.cpp/build/bin/llama-cli")
LLAMA_MODEL = os.path.expanduser(
    "~/llama.cpp/models/mistral-7b-instruct-v0.1.Q4_K_M.gguf")

AUDIO_FILE = "my_voice.wav"
MEMORY_FILE = "memory.json"

# === Load & Save Memory ===


def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return []


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

# === Transcribe with Whisper ===


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

# === Ask LLaMA ===


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


# === Main ===
if __name__ == "__main__":
    print("🎙️ Welcome to MemoryMate v0.1 (Offline AI)")
    record_voice(filename=AUDIO_FILE, duration=5)
    user_text = transcribe(AUDIO_FILE)
    if user_text:
        response = query_llama(user_text)

        # Save to memory
        memory = load_memory()
        memory.append(f"User: {user_text}\nAssistant: {response}")
        save_memory(memory)
