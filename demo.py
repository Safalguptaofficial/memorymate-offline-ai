#!/usr/bin/env python3
"""
MemoryMate Demo Script
Showcases the core features without requiring AI models
"""

import time
from datetime import datetime, timedelta
from task_manager import Task, Priority, TaskStatus, TaskManager
from memory_store import MemoryStore


def print_banner():
    """Print demo banner"""
    print("""
🧠 MemoryMate Demo
🎯 Showcasing your offline AI productivity assistant
🔒 100% Offline • 💬 Voice-powered • 🧠 Locally intelligent
    """)


def demo_task_management():
    """Demonstrate task management features"""
    print("\n📋 Task Management Demo")
    print("=" * 50)
    
    # Initialize task manager
    task_manager = TaskManager("demo.db")
    
    # Create sample tasks
    sample_tasks = [
        {
            "title": "Call mom tomorrow evening",
            "description": "Check in and see how she's doing",
            "due_date": (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
            "priority": Priority.IMPORTANT_NOT_URGENT,
            "tags": ["personal", "call"]
        },
        {
            "title": "Finish quarterly report by Friday",
            "description": "Complete the Q4 financial analysis",
            "due_date": (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'),
            "priority": Priority.URGENT_IMPORTANT,
            "tags": ["work", "report", "urgent"]
        },
        {
            "title": "Buy groceries",
            "description": "Milk, bread, eggs, and vegetables",
            "due_date": datetime.now().strftime('%Y-%m-%d'),
            "priority": Priority.OPTIONAL,
            "tags": ["personal", "shopping"]
        },
        {
            "title": "Study for exam next week",
            "description": "Review chapters 5-8 and practice problems",
            "due_date": (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
            "priority": Priority.IMPORTANT_NOT_URGENT,
            "tags": ["study", "exam"]
        }
    ]
    
    print("🚀 Creating sample tasks...")
    for task_data in sample_tasks:
        task = Task(
            id=None,
            title=task_data["title"],
            description=task_data["description"],
            due_date=task_data["due_date"],
            priority=task_data["priority"],
            status=TaskStatus.PENDING,
            tags=task_data["tags"],
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        task_id = task_manager.add_task(task)
        print(f"   ✅ Added: {task.title}")
    
    # Display all tasks
    print("\n📊 All Tasks:")
    all_tasks = task_manager.get_all_tasks()
    for i, task in enumerate(all_tasks, 1):
        priority_emoji = "🔴" if task.priority == Priority.URGENT_IMPORTANT else "🟡" if task.priority == Priority.IMPORTANT_NOT_URGENT else "🟢"
        status_emoji = "✅" if task.status == TaskStatus.COMPLETED else "⏳" if task.status == TaskStatus.IN_PROGRESS else "📝"
        
        print(f"\n{i}. {priority_emoji} {status_emoji} {task.title}")
        if task.description:
            print(f"   📝 {task.description}")
        if task.due_date:
            print(f"   📅 Due: {task.due_date}")
        if task.tags:
            print(f"   🏷️  Tags: {', '.join(task.tags)}")
    
    # Demonstrate filtering
    print("\n🔍 Filtering Demo:")
    
    # By priority
    urgent_tasks = task_manager.get_tasks_by_priority(Priority.URGENT_IMPORTANT)
    print(f"   🔴 Urgent & Important: {len(urgent_tasks)} tasks")
    
    # By status
    pending_tasks = task_manager.get_tasks_by_status(TaskStatus.PENDING)
    print(f"   📝 Pending: {len(pending_tasks)} tasks")
    
    # Search
    search_results = task_manager.search_tasks("report")
    print(f"   🔍 Search 'report': {len(search_results)} tasks")
    
    # Demonstrate task updates
    print("\n🔄 Task Updates Demo:")
    
    # Mark first task as in progress
    if all_tasks:
        first_task = all_tasks[0]
        first_task.status = TaskStatus.IN_PROGRESS
        first_task.updated_at = datetime.now().isoformat()
        task_manager.update_task(first_task)
        print(f"   ⏳ Started working on: {first_task.title}")
    
    # Mark second task as completed
    if len(all_tasks) > 1:
        second_task = all_tasks[1]
        second_task.status = TaskStatus.COMPLETED
        second_task.updated_at = datetime.now().isoformat()
        task_manager.update_task(second_task)
        print(f"   ✅ Completed: {second_task.title}")
    
    # Show updated status
    print("\n📊 Updated Task Status:")
    updated_tasks = task_manager.get_all_tasks()
    for i, task in enumerate(updated_tasks, 1):
        priority_emoji = "🔴" if task.priority == Priority.URGENT_IMPORTANT else "🟡" if task.priority == Priority.IMPORTANT_NOT_URGENT else "🟢"
        status_emoji = "✅" if task.status == TaskStatus.COMPLETED else "⏳" if task.status == TaskStatus.IN_PROGRESS else "📝"
        
        print(f"{i}. {priority_emoji} {status_emoji} {task.title}")
    
    task_manager.close()
    return all_tasks


def demo_memory_system():
    """Demonstrate the memory system"""
    print("\n🧠 Memory System Demo")
    print("=" * 50)
    
    # Create memory store
    memory_store = MemoryStore("demo.db")
    
    # Add sample memories
    print("💾 Adding sample memories...")
    sample_memories = [
        "User: Remind me to call mom tomorrow evening about dinner plans",
        "Assistant: I've added the task 'Call mom' to your list for tomorrow evening",
        "User: What's on my plate today?",
        "Assistant: You have 3 tasks due today: Buy groceries, Call mom, and Study for exam",
        "User: I promised Rohan I'd send the project report by Monday",
        "Assistant: I'll add that to your tasks. Due Monday, priority set to urgent",
        "User: Show me my urgent tasks",
        "Assistant: You have 2 urgent tasks: Finish quarterly report and Send project report to Rohan"
    ]
    
    for memory in sample_memories:
        memory_id = memory_store.add_memory(memory)
        print(f"   ✅ Added: {memory[:50]}...")
    
    # Demonstrate memory recall
    print("\n🔍 Memory Recall Demo:")
    
    # Search for specific information
    query = "What did I promise Rohan?"
    print(f"\n🔍 Query: '{query}'")
    memories = memory_store.search_memory(query, limit=2)
    
    if memories:
        print("   📝 Found memories:")
        for memory in memories:
            print(f"      • {memory['text'][:80]}...")
    else:
        print("   ❌ No memories found for this query")
    
    # Search for another query
    query2 = "call mom"
    print(f"\n🔍 Query: '{query2}'")
    memories2 = memory_store.search_memory(query2, limit=3)
    
    if memories2:
        print("   📝 Found memories:")
        for memory in memories2:
            print(f"      • {memory['text'][:80]}...")
    else:
        print("   ❌ No memories found for this query")
    
    # Show recent memories
    print(f"\n📝 Recent memories (last 5):")
    recent_memories = memory_store.get_recent_memories(5)
    for memory in recent_memories:
        print(f"   • {memory['text'][:60]}...")
    
    # Show memory statistics
    total_memories = memory_store.get_memory_count()
    print(f"\n📊 Memory Statistics:")
    print(f"   • Total memories: {total_memories}")
    print(f"   • Memory system working: ✅")
    
    print("\n✅ Memory System Demo Complete!")


def demo_ai_assistant():
    """Demonstrate AI assistant features"""
    print("\n🤖 AI Assistant Demo")
    print("=" * 50)
    
    print("🎯 Intent Classification Demo:")
    
    # Sample user inputs and their classified intents
    sample_inputs = [
        ("Remind me to call mom tomorrow", "add_task"),
        ("What's on my plate today?", "list_tasks"),
        ("Mark task 1 as complete", "complete_task"),
        ("Search for study tasks", "search_tasks"),
        ("What did I promise Rohan?", "recall_memory"),
        ("Hello, how are you?", "greeting"),
        ("Help me understand what you can do", "help"),
        ("Tell me a joke", "general_chat")
    ]
    
    for user_input, expected_intent in sample_inputs:
        print(f"   🎤 '{user_input}' → Intent: {expected_intent}")
    
    print("\n💬 Natural Language Processing:")
    print("   • Automatic intent detection")
    print("   • Smart task parsing")
    print("   • Context-aware responses")
    print("   • Memory integration")
    
    print("\n🎯 Task Parsing Examples:")
    parsing_examples = [
        "Remind me to call mom tomorrow evening",
        "I need to finish the report by Friday, it's urgent",
        "Buy groceries today",
        "Study for exam next week"
    ]
    
    for example in parsing_examples:
        print(f"   🎤 '{example}'")
        print(f"      📝 Would be parsed into structured task with:")
        print(f"         • Title, description, due date")
        print(f"         • Automatic priority detection")
        print(f"         • Smart tagging and categorization")


def demo_focus_mode():
    """Demonstrate focus mode features"""
    print("\n🎯 Focus Mode Demo")
    print("=" * 50)
    
    print("🎯 Focus Mode Features:")
    print("   • Single task focus for maximum productivity")
    print("   • Built-in Pomodoro timer (25/5/15 minute cycles)")
    print("   • AI motivation and productivity tips")
    print("   • Progress tracking and completion")
    
    print("\n⏰ Timer Demo:")
    print("   🍅 25-minute work session")
    print("   ☕ 5-minute short break")
    print("   🛌 15-minute long break")
    print("   🔄 Automatic session management")
    
    print("\n💪 Productivity Features:")
    print("   • Task status management (Start, Complete, Snooze)")
    print("   • Focus session analytics")
    print("   • Distraction blocking")
    print("   • Achievement tracking")


def demo_voice_features():
    """Demonstrate voice interaction features"""
    print("\n🎤 Voice Features Demo")
    print("=" * 50)
    
    print("🎙️ Voice Input:")
    print("   • Voice Activity Detection (VAD)")
    print("   • Automatic recording start/stop")
    print("   • High-quality audio capture")
    print("   • Noise filtering and optimization")
    
    print("\n🔊 Text-to-Speech:")
    print("   • Natural voice responses")
    print("   • Adjustable speech rate and volume")
    print("   • Multiple voice options")
    print("   • Cross-platform compatibility")
    
    print("\n💬 Voice Commands:")
    voice_commands = [
        "Remind me to call mom tomorrow evening",
        "What's on my plate today?",
        "Mark task 1 as complete",
        "Start focus mode on current task",
        "Give me my daily summary"
    ]
    
    for command in voice_commands:
        print(f"   🎤 '{command}'")
    
    print("\n🔧 Voice Settings:")
    print("   • Speech rate: 100-300 words per minute")
    print("   • Volume: 0-100%")
    print("   • Voice selection: Male/Female options")
    print("   • Language support: Multiple languages")


def demo_web_interface():
    """Demonstrate web interface features"""
    print("\n🌐 Web Interface Demo")
    print("=" * 50)
    
    print("🖥️ Streamlit Web App:")
    print("   • Modern, responsive design")
    print("   • Real-time task updates")
    print("   • Interactive task management")
    print("   • Beautiful visualizations")
    
    print("\n📊 Dashboard Features:")
    print("   • Task overview with metrics")
    print("   • Priority-based task organization")
    print("   • Quick add task form")
    print("   • Filter and search capabilities")
    
    print("\n💬 AI Chat Interface:")
    print("   • Natural language conversation")
    print("   • Quick action buttons")
    print("   • Chat history persistence")
    print("   • Voice response options")
    
    print("\n🎨 UI Components:")
    print("   • Task cards with priority colors")
    print("   • Status badges and indicators")
    print("   • Progress bars and metrics")
    print("   • Responsive layout design")


def main():
    """Main demo function"""
    print_banner()
    
    print("🎯 This demo showcases MemoryMate's core features")
    print("💡 No AI models required - just the core functionality")
    
    # Run demos
    demo_task_management()
    demo_memory_system()
    demo_ai_assistant()
    demo_focus_mode()
    demo_voice_features()
    demo_web_interface()
    
    print("\n" + "=" * 60)
    print("🎉 Demo Complete!")
    print("=" * 60)
    
    print("\n🚀 To experience the full MemoryMate:")
    print("1. Run: python setup.py")
    print("2. Setup Whisper.cpp and LLaMA.cpp")
    print("3. Download AI models")
    print("4. Run: python main.py")
    print("5. Or web UI: streamlit run streamlit_app.py")
    
    print("\n💡 Key Benefits:")
    print("   • 100% offline - works without internet")
    print("   • Voice-first interaction - natural and intuitive")
    print("   • AI-powered task management - smart and efficient")
    print("   • Privacy-focused - all data stays on your device")
    print("   • Cross-platform - works on macOS, Linux, and Windows")
    
    print("\n🧠 MemoryMate - Making productivity feel natural and human!")
    print("🔒 Built for the offline-first, privacy-conscious productivity enthusiast.")


if __name__ == "__main__":
    main()
