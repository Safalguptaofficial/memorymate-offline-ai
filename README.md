# 🧠 MemoryMate – Offline AI Task Manager & Personal Assistant

> 🔒 100% Offline • 💬 Voice-powered • 🧠 Locally intelligent • 🎯 Productivity-focused

MemoryMate is your offline-first AI productivity assistant that helps you capture ideas, manage tasks, and stay productive — even without the internet. It combines speech recognition (Whisper), reasoning (LLaMA), memory (FAISS), and voice interaction (TTS) to create a human-like personal assistant.

Think of it as a **Jarvis-style AI for task management** that works fully on your laptop.

## ✨ Core Features

### 🎤 Voice-First Task Capture
- **Natural Language Processing**: Speak naturally like "Remind me to call mom tomorrow evening"
- **AI Task Parsing**: Automatically extracts title, due date, priority, and tags
- **Voice Activity Detection**: Smart recording that starts/stops based on speech
- **Text-to-Speech**: AI responds with both text and voice

### 🎯 Intelligent Task Management
- **AI Prioritization**: Tasks automatically ranked by urgency/importance
- **Smart Categorization**: Automatic tagging and organization
- **Due Date Detection**: Understands natural time references
- **Priority Levels**: Urgent & Important, Important, Optional

### 🧠 Memory & Context
- **Semantic Memory**: FAISS-powered vector search for task recall
- **Conversation History**: Remembers your preferences and context
- **Smart Search**: Find tasks by meaning, not just keywords
- **Personal Insights**: Learns from your productivity patterns

### 🎯 Focus Mode
- **Single Task Focus**: Work on one task at a time
- **Pomodoro Timer**: Built-in productivity timer
- **AI Motivation**: Personalized productivity tips and encouragement
- **Progress Tracking**: Visual progress indicators

### 💬 Natural AI Chat
- **Conversational Interface**: Chat naturally about your tasks
- **Task Queries**: "What's on my plate today?" or "Show urgent tasks"
- **Memory Recall**: "What did I promise Rohan last week?"
- **Productivity Insights**: Get AI-powered productivity advice

## 🛠️ Tech Stack

### Core AI Models
- **🎤 Speech Recognition**: `whisper.cpp` (ggml-base.en.bin)
- **🧠 Language Model**: `llama.cpp` (Mistral 7B Instruct GGUF)
- **🔍 Vector Memory**: `FAISS` + `sentence-transformers` (all-MiniLM-L6-v2)
- **🔊 Text-to-Speech**: `pyttsx3` (offline, cross-platform)

### Backend & Storage
- **Database**: SQLite with automatic schema management
- **Memory System**: FAISS vector database for semantic search
- **Task Engine**: Intelligent task parsing and prioritization
- **Audio Processing**: WebRTC VAD for voice activity detection

### User Interfaces
- **Terminal App**: Rich CLI with interactive menus
- **Web Interface**: Streamlit-based modern web UI
- **Voice Interface**: Natural voice commands and responses

## 🚀 Quick Start

### 1. Install Dependencies
```bash
# Run the setup script
python setup.py

# Or install manually
pip install -r requirements.txt
```

### 2. Setup AI Models
```bash
# Clone and build Whisper.cpp
git clone https://github.com/ggerganov/whisper.cpp.git
cd whisper.cpp && make
# Download ggml-base.en.bin to models/ folder

# Clone and build LLaMA.cpp
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp && make
# Download mistral-7b-instruct-v0.1.Q4_K_M.gguf to models/ folder
```

### 3. Run MemoryMate
```bash
# Terminal interface
python main.py

# Web interface
streamlit run streamlit_app.py
```

## 📱 Usage Examples

### Voice Commands
```
🎤 "Remind me to call mom tomorrow evening"
🧠 Creates: Task "Call mom" | Due: tomorrow | Priority: Important

🎤 "I need to finish the report by Friday, it's urgent"
🧠 Creates: Task "Finish report" | Due: Friday | Priority: Urgent & Important

🎤 "What's on my plate today?"
🧠 Lists: All tasks due today with priorities and status
```

### Text Commands
```
📝 "Add task: Buy groceries tomorrow"
📝 "Show my urgent tasks"
📝 "Mark task 1 as complete"
📝 "Search for study tasks"
📝 "What did I promise Rohan last week?"
```

### Focus Mode
```
🎯 Start focus session on current task
⏰ 25-minute Pomodoro timer
🍅 Break reminders and motivation
✅ Mark completion with voice
```

## 🏗️ Architecture

```
memorymate-offline-ai/
├── 🧠 ai_assistant.py          # Main AI logic and intent handling
├── 📋 task_manager.py          # Task CRUD and AI parsing
├── 🗄️ memory_store.py          # FAISS vector memory system
├── 🎤 vad_module.py            # Voice activity detection
├── 🔊 tts.py                   # Text-to-speech engine
├── 🎙️ transcribe_and_respond.py # Whisper + LLaMA integration
├── 🖥️ main.py                  # Terminal CLI interface
├── 🌐 streamlit_app.py         # Web UI interface
├── ⚙️ setup.py                 # Installation and setup script
├── 📦 requirements.txt         # Python dependencies
└── 📚 README.md                # This file
```

## 🔧 Configuration

### Environment Variables
```bash
# Optional: Custom database path
export MEMORYMATE_DB_PATH="/path/to/custom/database.db"

# Optional: Custom model paths
export WHISPER_MODEL_PATH="./whisper.cpp/models/ggml-base.en.bin"
export LLAMA_MODEL_PATH="./llama.cpp/models/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
```

### Customization
- **Voice Settings**: Adjust speech rate, volume, and voice selection
- **Task Priorities**: Modify priority detection logic
- **Memory Retention**: Configure FAISS index parameters
- **UI Themes**: Customize Streamlit appearance

## 🌟 Advanced Features

### AI-Powered Insights
- **Productivity Analytics**: Track completion rates and patterns
- **Smart Scheduling**: AI suggests optimal task timing
- **Context Awareness**: Understands task relationships
- **Personalization**: Learns your work style over time

### Integration Capabilities
- **Calendar Sync**: Google Calendar integration (optional)
- **Note Taking**: Attach voice notes and documents
- **Export Options**: CSV, JSON, and calendar exports
- **Backup System**: Local and cloud backup options

### Performance Optimizations
- **Lazy Loading**: Models load only when needed
- **Memory Management**: Efficient FAISS index handling
- **Audio Processing**: Optimized voice recording pipeline
- **Caching**: Smart caching for frequently accessed data

## 🐛 Troubleshooting

### Common Issues
```
❌ "No module named 'webrtcvad'"
💡 Install: pip install webrtcvad

❌ "Audio device not found"
💡 Check microphone permissions and system audio settings

❌ "Whisper transcription failed"
💡 Verify whisper.cpp is built and model is downloaded

❌ "LLaMA response error"
💡 Check llama.cpp build and model file location
```

### Performance Tips
- **Model Optimization**: Use quantized models for faster inference
- **Memory Usage**: Monitor FAISS index size and optimize
- **Audio Quality**: Use good microphone in quiet environment
- **System Resources**: Ensure sufficient RAM for AI models

## 🤝 Contributing

We welcome contributions! Here's how to help:

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Test** thoroughly
5. **Submit** a pull request

### Development Setup
```bash
git clone https://github.com/yourusername/memorymate-offline-ai.git
cd memorymate-offline-ai
python setup.py
# Make your changes
python -m pytest tests/  # Run tests
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Whisper.cpp**: Speech recognition by OpenAI
- **LLaMA.cpp**: Language model inference by Meta
- **FAISS**: Vector similarity search by Facebook Research
- **Streamlit**: Web app framework
- **Open Source Community**: For all the amazing tools and libraries

## 🎯 Roadmap

### Phase 2 (Next Release)
- [ ] Mobile companion app
- [ ] Advanced analytics dashboard
- [ ] Team collaboration features
- [ ] API for third-party integrations

### Phase 3 (Future)
- [ ] Multi-language support
- [ ] Advanced AI reasoning
- [ ] Predictive task suggestions
- [ ] Cross-platform sync

## 📞 Support

- **Documentation**: Check this README first
- **Issues**: Open a GitHub issue for bugs
- **Discussions**: Use GitHub Discussions for questions
- **Email**: [your-email@example.com]

---

**🧠 MemoryMate** - Making productivity feel natural and human, one task at a time.

*Built with ❤️ for the offline-first, privacy-conscious productivity enthusiast.*
