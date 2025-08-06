# 🎙️ MemoryMate v0.2 – Offline AI Assistant

> 🔒 100% Offline. 💬 Voice-powered. 🧠 Locally intelligent.

MemoryMate is a fully offline, privacy-preserving voice assistant that transcribes your speech using `Whisper.cpp`, interprets your commands using `LLaMA.cpp`, and responds—all without needing internet access.

---

## ✅ Phase 1 – Core Features

- 🎤 **Voice Recording**  
  Records your voice locally using your system’s microphone.

- 🧠 **Speech-to-Text via Whisper.cpp**  
  Converts your recorded voice to text using OpenAI’s Whisper model (offline).

- 🤖 **Local AI Response with LLaMA.cpp**  
  Sends the text to a local Mistral 7B model running on LLaMA.cpp and gets a smart response.

- 🔁 **Fully Offline**  
  No internet, no APIs, no tracking—everything happens on your device.

---

## 🚧 Phase 2 – In Progress

- 🔊 **Text-to-Speech (TTS)**  
  AI speaks back using tools like `say`, `espeak`, or Coqui TTS.

- 🖥️ **GUI / Web App**  
  Launch a clean frontend using **Streamlit** or **Gradio**.

- 📖 **Memory Persistence**  
  Add context memory using `memory.json` so the assistant remembers previous chats.

- 🧹 **GitHub Polish**  
  Improved documentation and visuals for better impact (e.g., Samsung Hackathon).

---

## 📂 Folder Structure

```
memorymate-offline-ai/
├── main.py               # Orchestrates all voice-to-AI interaction
├── record.py             # Microphone audio recording
├── memory.json           # Stores conversation memory
├── README.md             # This file
├── .gitignore
├── LICENSE
├── whisper.cpp/          # Cloned & built Whisper.cpp
└── llama.cpp/            # Cloned & built LLaMA.cpp
```

---

## 🛠️ Setup Instructions

### 1. Install Requirements

- Python 3.10+
- `ffmpeg` (`brew install ffmpeg` on macOS)
- C++ compiler (for building Whisper and LLaMA)

### 2. Build Dependencies

Clone and build:

- [Whisper.cpp](https://github.com/ggerganov/whisper.cpp)
- [LLaMA.cpp](https://github.com/ggerganov/llama.cpp)

### 3. Download Models

- Whisper: [`ggml-base.en.bin`](https://huggingface.co/ggerganov/whisper.cpp)
- LLaMA: `mistral-7b-instruct-v0.1.Q4_K_M.gguf` (via HuggingFace or other)

Place them in:

- `~/whisper.cpp/models/`
- `~/llama.cpp/models/`

---

## ▶️ Run the App

```bash
python3 main.py
```

Speak when prompted 🎤  
Your voice → Transcription → LLaMA AI response 🧠

---

## 💡 Use Cases

- 💬 Offline Chatbot
- 🔐 Privacy-first AI Assistant
- 👩‍⚕️ Healthcare or Elder Care Tool
- 🏫 Education Companion

---

## 🎯 Why It Matters

This project was built with privacy, speed, and offline usability in mind—perfect for:

- 🌐 Low-connectivity environments
- 📱 On-device AI deployments
- 💻 Hackathons & Prototypes (e.g., Samsung Hackathon)

---

## 🤝 Contributing

Have ideas or want to improve it?  
Open an issue or submit a pull request.

---

## 📜 License

MIT License – see [LICENSE](LICENSE) for full details.
