# transcribe_and_respond.py
import os


def transcribe_with_whisper(audio_file):
    print("🧠 Transcribing with Whisper.cpp...")
    os.system(f"./main -m models/ggml-base.en.bin -f {audio_file} -otxt")
    text_file = f"{audio_file}.txt"
    with open(text_file, "r") as f:
        transcript = f.read().strip()
    return transcript


def generate_llama_response(user_input):
    print("🤖 Asking LLaMA...")
    with open("prompt.txt", "w") as f:
        f.write(user_input)

    os.system("./llama/main -m ./models/7B/ggml-model-q4_0.bin -p prompt.txt -n 200")

    # Assuming LLaMA writes to stdout or to a file
    # If output goes to a file, read from it here
    # Example:
    # with open("llama_output.txt", "r") as f:
    #     response = f.read().strip()
    # return response

    # If output appears in terminal, optionally return placeholder:
    return "(LLaMA output shown in terminal)"
