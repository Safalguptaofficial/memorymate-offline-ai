#!/usr/bin/env python3
"""
MemoryMate Setup Script
Installs dependencies and sets up the environment for MemoryMate
"""

import os
import sys
import subprocess
import platform
import shutil


def print_banner():
    """Print setup banner"""
    print("""
🧠 MemoryMate Setup Script
🎯 Setting up your offline AI productivity assistant
🔒 100% Offline • 💬 Voice-powered • 🧠 Locally intelligent
    """)


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True


def install_pip_packages():
    """Install required Python packages"""
    print("\n📦 Installing Python packages...")
    
    packages = [
        "streamlit>=1.28.0",
        "pyttsx3>=2.90",
        "sounddevice>=0.4.6",
        "scipy>=1.11.0",
        "numpy>=1.24.0",
        "webrtcvad>=2.0.10",
        "faiss-cpu>=1.7.4",
        "sentence-transformers>=2.2.2",
        "plotly>=5.17.0",
        "pandas>=2.0.0"
    ]
    
    for package in packages:
        try:
            print(f"   Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"   ✅ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Failed to install {package}: {e}")
            return False
    
    return True


def check_system_dependencies():
    """Check for system dependencies"""
    print("\n🔧 Checking system dependencies...")
    
    system = platform.system()
    
    if system == "Darwin":  # macOS
        print("🐧 macOS detected")
        
        # Check for Homebrew
        if not shutil.which("brew"):
            print("   ⚠️  Homebrew not found")
            print("   💡 Install Homebrew: https://brew.sh/")
            print("   💡 Then run: brew install ffmpeg portaudio")
        else:
            print("   ✅ Homebrew found")
            
            # Check for ffmpeg
            if not shutil.which("ffmpeg"):
                print("   ⚠️  ffmpeg not found")
                print("   💡 Install with: brew install ffmpeg")
            else:
                print("   ✅ ffmpeg found")
            
            # Check for portaudio
            if not shutil.which("portaudio"):
                print("   ⚠️  portaudio not found")
                print("   💡 Install with: brew install portaudio")
            else:
                print("   ✅ portaudio found")
    
    elif system == "Linux":
        print("🐧 Linux detected")
        
        # Check for ffmpeg
        if not shutil.which("ffmpeg"):
            print("   ⚠️  ffmpeg not found")
            print("   💡 Install with: sudo apt-get install ffmpeg")
        else:
            print("   ✅ ffmpeg found")
        
        # Check for portaudio
        if not shutil.which("portaudio"):
            print("   ⚠️  portaudio not found")
            print("   💡 Install with: sudo apt-get install portaudio19-dev")
        else:
            print("   ✅ portaudio found")
    
    elif system == "Windows":
        print("🪟 Windows detected")
        print("   💡 Make sure you have Visual C++ build tools installed")
        print("   💡 Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/")
    
    return True


def setup_whisper_llama():
    """Setup instructions for Whisper.cpp and LLaMA.cpp"""
    print("\n🤖 AI Model Setup")
    print("=" * 50)
    print("""
MemoryMate requires two AI models to work:

1. 🎤 Whisper.cpp (Speech-to-Text)
   • Clone: git clone https://github.com/ggerganov/whisper.cpp.git
   • Build: cd whisper.cpp && make
   • Download model: Download ggml-base.en.bin to models/ folder
   • Place in: ./whisper.cpp/models/

2. 🧠 LLaMA.cpp (Language Model)
   • Clone: git clone https://github.com/ggerganov/llama.cpp.git
   • Build: cd llama.cpp && make
   • Download model: Download mistral-7b-instruct-v0.1.Q4_K_M.gguf
   • Place in: ./llama.cpp/models/

3. 📁 Expected folder structure:
   memorymate-offline-ai/
   ├── whisper.cpp/
   │   ├── main (executable)
   │   └── models/
   │       └── ggml-base.en.bin
   └── llama.cpp/
       ├── main (executable)
       └── models/
           └── mistral-7b-instruct-v0.1.Q4_K_M.gguf

⚠️  Note: These models are large (several GB) and may take time to download.
    """)
    
    # Check if directories exist
    if os.path.exists("whisper.cpp") and os.path.exists("llama.cpp"):
        print("✅ Whisper.cpp and LLaMA.cpp directories found")
        
        # Check for executables
        if os.path.exists("whisper.cpp/main") or os.path.exists("whisper.cpp/main.exe"):
            print("✅ Whisper.cpp executable found")
        else:
            print("❌ Whisper.cpp executable not found - needs to be built")
        
        if os.path.exists("llama.cpp/main") or os.path.exists("llama.cpp/main.exe"):
            print("✅ LLaMA.cpp executable found")
        else:
            print("❌ LLaMA.cpp executable not found - needs to be built")
    else:
        print("❌ Whisper.cpp and/or LLaMA.cpp directories not found")
        print("   💡 Please clone and build them as described above")


def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = [
        "models",
        "recordings",
        "exports"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"   ✅ Created {directory}/")
        else:
            print(f"   ✅ {directory}/ already exists")


def test_installation():
    """Test if the installation works"""
    print("\n🧪 Testing installation...")
    
    try:
        # Test imports
        print("   Testing imports...")
        import streamlit
        import pyttsx3
        import sounddevice
        import numpy
        import faiss
        import sentence_transformers
        print("   ✅ All Python packages imported successfully")
        
        # Test TTS
        print("   Testing text-to-speech...")
        import tts
        print("   ✅ TTS module loaded successfully")
        
        # Test task manager
        print("   Testing task manager...")
        import task_manager
        print("   ✅ Task manager module loaded successfully")
        
        # Test AI assistant
        print("   Testing AI assistant...")
        import ai_assistant
        print("   ✅ AI assistant module loaded successfully")
        
        print("✅ All tests passed! MemoryMate is ready to use.")
        return True
        
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def print_next_steps():
    """Print next steps for the user"""
    print("\n🚀 Next Steps")
    print("=" * 50)
    print("""
1. 📥 Download AI Models:
   • Whisper: https://huggingface.co/ggerganov/whisper.cpp
   • LLaMA: https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF

2. 🏗️ Build Dependencies:
   • Follow the setup instructions above for Whisper.cpp and LLaMA.cpp

3. 🎯 Run MemoryMate:
   • Terminal: python main.py
   • Web UI: streamlit run streamlit_app.py

4. 🎤 Test Voice Input:
   • Make sure your microphone is working
   • Speak clearly in a quiet environment

5. 📚 Read the README:
   • Check README.md for detailed usage instructions

Need help? Check the README or open an issue on GitHub!
    """)


def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install Python packages
    if not install_pip_packages():
        print("❌ Failed to install Python packages")
        sys.exit(1)
    
    # Check system dependencies
    check_system_dependencies()
    
    # Setup AI models
    setup_whisper_llama()
    
    # Create directories
    create_directories()
    
    # Test installation
    if not test_installation():
        print("❌ Installation test failed")
        print("💡 Please check the error messages above")
        sys.exit(1)
    
    # Print next steps
    print_next_steps()
    
    print("\n🎉 Setup complete! MemoryMate is ready to use.")
    print("🧠 Happy productivity!")


if __name__ == "__main__":
    main()
