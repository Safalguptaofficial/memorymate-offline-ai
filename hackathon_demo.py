#!/usr/bin/env python3
"""
🧠 MemoryMate - Hackathon Demo Script
Award-winning offline AI productivity assistant demo

This script demonstrates all the key features that make MemoryMate special:
- Offline-first architecture
- AI-powered task management
- Voice interaction capabilities
- Memory system
- Focus mode
- Beautiful UI/UX
"""

import time
import random
from datetime import datetime, timedelta
from task_manager import Task, Priority, TaskStatus, TaskManager, AITaskParser
from memory_store import MemoryStore
from ai_assistant import MemoryMateAssistant
from tts import speak_text
import streamlit as st

class HackathonDemo:
    """Comprehensive demo for hackathon presentation"""
    
    def __init__(self):
        self.task_manager = TaskManager()
        self.memory_store = MemoryStore()
        self.assistant = MemoryMateAssistant()
        self.demo_data_created = False
        
    def print_banner(self):
        """Print the MemoryMate banner"""
        print("=" * 80)
        print("🧠 MEMORYMATE - OFFLINE AI PRODUCTIVITY ASSISTANT 🧠")
        print("=" * 80)
        print("🏆 HACKATHON DEMO - AWARD-WINNING FEATURES")
        print("=" * 80)
        print()
        
    def create_demo_data(self):
        """Create sample data for the demo"""
        if self.demo_data_created:
            return
            
        print("📊 Creating demo data...")
        
        # Sample tasks
        tasks = [
            Task(
                id=None,
                title="Complete hackathon project",
                description="Finish MemoryMate demo and prepare presentation",
                due_date=(datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
                priority=Priority.URGENT_IMPORTANT,
                status=TaskStatus.IN_PROGRESS,
                tags=["hackathon", "urgent", "project"],
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            ),
            Task(
                id=None,
                title="Practice presentation",
                description="Rehearse demo flow and key talking points",
                due_date=datetime.now().strftime('%Y-%m-%d'),
                priority=Priority.URGENT_IMPORTANT,
                status=TaskStatus.PENDING,
                tags=["hackathon", "presentation"],
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            ),
            Task(
                id=None,
                title="Research competitors",
                description="Analyze other productivity apps in the market",
                due_date=(datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'),
                priority=Priority.IMPORTANT_NOT_URGENT,
                status=TaskStatus.PENDING,
                tags=["research", "market-analysis"],
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            ),
            Task(
                id=None,
                title="Update portfolio",
                description="Add MemoryMate to personal portfolio website",
                due_date=(datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
                priority=Priority.OPTIONAL,
                status=TaskStatus.PENDING,
                tags=["portfolio", "personal"],
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            )
        ]
        
        # Add tasks
        for task in tasks:
            self.task_manager.add_task(task)
            
        # Add sample memories
        memories = [
            "User: I need to focus on the hackathon project today",
            "User: The AI task prioritization is working really well",
            "User: Voice input would be amazing for quick task capture",
            "User: The offline-first approach is perfect for privacy",
            "User: I love how the AI remembers my preferences"
        ]
        
        for memory in memories:
            self.memory_store.add_memory(memory)
            
        self.demo_data_created = True
        print("✅ Demo data created successfully!")
        print()
        
    def demo_offline_first(self):
        """Demonstrate offline-first capabilities"""
        print("🔒 DEMO: Offline-First Architecture")
        print("-" * 50)
        print("✅ No internet connection required")
        print("✅ All data stored locally on device")
        print("✅ AI models run completely offline")
        print("✅ 100% private - no data leaves your device")
        print("✅ Works in airplanes, remote locations, anywhere!")
        print()
        
    def demo_ai_task_management(self):
        """Demonstrate AI-powered task management"""
        print("🤖 DEMO: AI-Powered Task Management")
        print("-" * 50)
        
        # Show current tasks
        all_tasks = self.task_manager.get_all_tasks()
        print(f"📋 Total tasks: {len(all_tasks)}")
        
        # Show AI prioritization
        urgent_tasks = [t for t in all_tasks if t.priority == Priority.URGENT_IMPORTANT]
        important_tasks = [t for t in all_tasks if t.priority == Priority.IMPORTANT_NOT_URGENT]
        optional_tasks = [t for t in all_tasks if t.priority == Priority.OPTIONAL]
        
        print(f"🔴 Urgent & Important: {len(urgent_tasks)}")
        print(f"🟡 Important (not urgent): {len(important_tasks)}")
        print(f"🟢 Optional: {len(optional_tasks)}")
        print()
        
        # Show AI parsing example
        print("🧠 AI Task Parsing Example:")
        sample_input = "Remind me to call mom tomorrow evening about dinner plans"
        print(f"Input: '{sample_input}'")
        
        parser = AITaskParser()
        parsed_task = parser.parse_task(sample_input)
        print(f"Parsed: Title='{parsed_task.title}', Due='{parsed_task.due_date}', Priority='{parsed_task.priority.value}'")
        print()
        
    def demo_memory_system(self):
        """Demonstrate the memory system"""
        print("🧠 DEMO: AI Memory System")
        print("-" * 50)
        
        # Show memory count
        memory_count = self.memory_store.get_memory_count()
        print(f"💾 Total memories stored: {memory_count}")
        
        # Show recent memories
        recent_memories = self.memory_store.get_recent_memories(3)
        print("📝 Recent memories:")
        for memory in recent_memories:
            print(f"   • {memory['text']}")
        print()
        
        # Show memory search
        print("🔍 Memory Search Example:")
        search_results = self.memory_store.search_memory("hackathon")
        print(f"Searching for 'hackathon': {len(search_results)} results found")
        for result in search_results:
            print(f"   • {result['text']}")
        print()
        
    def demo_voice_features(self):
        """Demonstrate voice interaction capabilities"""
        print("🎤 DEMO: Voice Interaction Features")
        print("-" * 50)
        print("✅ Voice Activity Detection (VAD)")
        print("✅ Smart audio recording")
        print("✅ Whisper.cpp integration (offline STT)")
        print("✅ Natural language task parsing")
        print("✅ Text-to-Speech responses")
        print("✅ Voice commands for task management")
        print()
        
        # Demo TTS
        print("🔊 Text-to-Speech Demo:")
        demo_text = "Hello! I'm MemoryMate, your AI productivity assistant."
        print(f"Speaking: '{demo_text}'")
        try:
            speak_text(demo_text)
            print("✅ TTS working!")
        except Exception as e:
            print(f"⚠️ TTS demo: {e}")
        print()
        
    def demo_focus_mode(self):
        """Demonstrate focus mode"""
        print("🎯 DEMO: Focus Mode")
        print("-" * 50)
        print("✅ Single-task focus")
        print("✅ Pomodoro timer integration")
        print("✅ AI motivation and tips")
        print("✅ Distraction-free interface")
        print("✅ Progress tracking")
        print()
        
        # Show current focus task
        in_progress_tasks = [t for t in self.task_manager.get_all_tasks() if t.status == TaskStatus.IN_PROGRESS]
        if in_progress_tasks:
            focus_task = in_progress_tasks[0]
            print(f"🎯 Current focus: {focus_task.title}")
            print(f"   Priority: {focus_task.priority.value}")
            print(f"   Status: {focus_task.status.value}")
        else:
            print("📝 No tasks currently in focus mode")
        print()
        
    def demo_ai_assistant(self):
        """Demonstrate AI assistant capabilities"""
        print("🤖 DEMO: AI Assistant")
        print("-" * 50)
        
        # Test AI responses
        test_queries = [
            "What's on my plate today?",
            "Show me urgent tasks",
            "What can you do?",
            "Give me a daily summary"
        ]
        
        for query in test_queries:
            print(f"❓ User: {query}")
            try:
                response = self.assistant.process_input(query)
                print(f"🤖 AI: {response}")
            except Exception as e:
                print(f"⚠️ AI response error: {e}")
            print()
            
    def demo_ui_features(self):
        """Demonstrate UI/UX features"""
        print("🎨 DEMO: Beautiful UI/UX")
        print("-" * 50)
        print("✅ Modern, responsive design")
        print("✅ Dark/Light mode toggle")
        print("✅ Smooth animations and transitions")
        print("✅ Mobile-friendly interface")
        print("✅ Intuitive navigation")
        print("✅ Gamification elements")
        print("✅ Progress tracking")
        print("✅ Beautiful charts and visualizations")
        print()
        
    def demo_technical_features(self):
        """Demonstrate technical capabilities"""
        print("⚙️ DEMO: Technical Features")
        print("-" * 50)
        print("✅ Cross-platform compatibility")
        print("✅ SQLite database")
        print("✅ Thread-safe operations")
        print("✅ Error handling and fallbacks")
        print("✅ Modular architecture")
        print("✅ Easy to extend and customize")
        print("✅ Performance optimized")
        print("✅ Memory efficient")
        print()
        
    def demo_hackathon_highlights(self):
        """Highlight what makes this hackathon project special"""
        print("🏆 HACKATHON HIGHLIGHTS")
        print("=" * 50)
        print("🎯 UNIQUE VALUE PROPOSITION:")
        print("   • First offline-first AI productivity assistant")
        print("   • Combines Whisper + LLaMA + FAISS + TTS")
        print("   • 100% private - no data collection")
        print("   • Works anywhere, anytime")
        print()
        
        print("🚀 INNOVATION:")
        print("   • Voice-first productivity interface")
        print("   • AI-powered task prioritization")
        print("   • Semantic memory system")
        print("   • Context-aware assistance")
        print()
        
        print("💡 TECHNICAL EXCELLENCE:")
        print("   • Modern tech stack (React/Streamlit)")
        print("   • Offline AI model integration")
        print("   • Beautiful, polished UI/UX")
        print("   • Scalable architecture")
        print()
        
        print("🎨 DESIGN EXCELLENCE:")
        print("   • Intuitive user experience")
        print("   • Beautiful visual design")
        print("   • Responsive and accessible")
        print("   • Gamification elements")
        print()
        
    def run_full_demo(self):
        """Run the complete hackathon demo"""
        self.print_banner()
        
        # Create demo data
        self.create_demo_data()
        
        # Run all demo sections
        self.demo_offline_first()
        time.sleep(1)
        
        self.demo_ai_task_management()
        time.sleep(1)
        
        self.demo_memory_system()
        time.sleep(1)
        
        self.demo_voice_features()
        time.sleep(1)
        
        self.demo_focus_mode()
        time.sleep(1)
        
        self.demo_ai_assistant()
        time.sleep(1)
        
        self.demo_ui_features()
        time.sleep(1)
        
        self.demo_technical_features()
        time.sleep(1)
        
        self.demo_hackathon_highlights()
        
        print("=" * 80)
        print("🎉 DEMO COMPLETE! MemoryMate is ready for the hackathon!")
        print("=" * 80)
        print()
        print("🚀 Next steps:")
        print("   1. Run: streamlit run streamlit_app.py")
        print("   2. Open browser to see the beautiful UI")
        print("   3. Test all features interactively")
        print("   4. Prepare your hackathon presentation!")
        print("=" * 80)
        
    def run_quick_demo(self):
        """Run a quick demo for time-constrained presentations"""
        self.print_banner()
        print("⚡ QUICK DEMO MODE")
        print("=" * 50)
        
        self.create_demo_data()
        
        # Quick highlights
        print("🔑 KEY FEATURES:")
        print("   • Offline-first AI productivity")
        print("   • Voice interaction with Whisper + LLaMA")
        print("   • Beautiful Streamlit UI")
        print("   • 100% private and secure")
        print()
        
        print("🎯 DEMO COMMANDS:")
        print("   • streamlit run streamlit_app.py")
        print("   • python demo.py")
        print("   • python quick_test.py")
        print()
        
        print("🏆 READY FOR HACKATHON!")

def main():
    """Main demo function"""
    demo = HackathonDemo()
    
    # Check if user wants quick demo
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        demo.run_quick_demo()
    else:
        demo.run_full_demo()

if __name__ == "__main__":
    main()
