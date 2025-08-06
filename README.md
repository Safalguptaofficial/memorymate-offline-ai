# 🧠 MemoryMate: Offline AI Voice Assistant

MemoryMate is an **offline AI voice assistant** that listens, remembers, and replies — all without an internet connection. Powered by [Whisper.cpp](https://github.com/ggerganov/whisper.cpp) for speech-to-text and [LLaMA.cpp](https://github.com/ggerganov/llama.cpp) for local language processing, it ensures **complete privacy** and blazing-fast performance.

---

## 🚀 Features

- 🎤 **Voice Input:** Speak naturally using your mic
- 🧠 **Long-Term Memory:** Remembers past interactions
- 🤖 **Natural Responses:** Replies using LLaMA-based local inference
- 🛡️ **Private:** Entirely offline, no data is ever sent to the cloud
- 🖥️ **Lightweight:** Runs smoothly on personal machines

---

## 📁 File Structure

```
memorymate-offline-ai/
├── main.py              # AI logic: processes and replies
├── record.py            # Records voice input to WAV
├── my_voice.wav         # Temporary recorded voice file
├── __pycache__/         # Python cache files
├── README.md            # This file
```

---

## 🛠️ Tech Stack

- **Python**
- **Whisper.cpp** – Local speech-to-text
- **LLaMA.cpp** – Local large language model
- **PyTorch** (optional)
- **NumPy**

---

## 🧪 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Safalguptaofficial/memorymate-offline-ai.git
cd memorymate-offline-ai
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Download models

- 📥 Download and set up:
  - Whisper model (for transcription)
  - LLaMA weights (for local inference)

Set correct model paths in `main.py` as needed.

---

## ▶️ Usage

### Step 1: Record your voice

```bash
python record.py
```

### Step 2: Let MemoryMate respond

```bash
python main.py
```

You’ll hear a smart AI reply that understands your prompt — all offline!

---

## 📈 Future Improvements

- GUI with voice visualizer
- Raspberry Pi integration
- Store memory logs in JSON or database
- Personal diary/chat history
- Real-time speech detection

---

## 📸 Screenshots / Demo (Coming Soon)

> Want to contribute a UI or GIF demo? Open a pull request!

---

## 👤 Author

**Safal Gupta**  
[@Safalguptaofficial](https://github.com/Safalguptaofficial)  
📍 Jaipur | 🏫 VIT Vellore | 🎓 CSE - IoT

---

## 📄 License

This project is licensed under the **MIT License**.  
Feel free to use, modify, and share it. Contributions are welcome!

---

### ⭐️ Support

If you find this project useful, consider giving it a ⭐️ on GitHub and sharing it with friends who love AI & privacy!
