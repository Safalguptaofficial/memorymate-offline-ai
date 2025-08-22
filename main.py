import os
import time
import sys
from vad_module import record_with_vad, record_simple
from transcribe_and_respond import transcribe_with_whisper, generate_llama_response
from tts import speak_text
from ai_assistant import MemoryMateAssistant
from task_manager import Task, Priority, TaskStatus, AITaskParser

AUDIO_FILE = "my_voice.wav"


def print_banner():
    """Print MemoryMate banner"""
    print("""
🧠 MemoryMate - Offline AI Productivity Assistant
🎯 Your personal Jarvis-style AI for task management
🔒 100% Offline • 💬 Voice-powered • 🧠 Locally intelligent
    """)


def print_menu():
    """Print main menu options"""
    print("""
📋 Main Menu:
1. 🎤 Voice Input - Speak to add tasks or chat
2. 📝 Text Input - Type your requests
3. 📊 View Tasks - See your current tasks
4. 🎯 Focus Mode - Work on one task at a time
5. 🔍 Search Tasks - Find specific tasks
6. 📅 Daily Summary - Get your daily overview
7. 💬 Chat Mode - Interactive conversation
8. ❓ Help - Learn what I can do
9. 🚪 Exit

Choose an option (1-9): """)


def voice_input_mode(assistant):
    """Handle voice input mode"""
    print("\n🎤 Voice Input Mode")
    print("💡 Speak clearly when prompted. Stay silent to stop recording.")
    
    try:
        # Try VAD recording first
        print("🎙️ Starting voice activity detection...")
        record_with_vad(AUDIO_FILE)
    except Exception as e:
        print(f"⚠️ VAD recording failed: {e}")
        print("🔄 Falling back to simple recording...")
        try:
            record_simple(AUDIO_FILE, 10)
        except Exception as e2:
            print(f"❌ Simple recording also failed: {e2}")
            print("💡 Please check your microphone and audio settings")
            return
    
    print(f"✅ Recording saved as '{AUDIO_FILE}'")
    
    # Transcribe
    print("🧠 Transcribing with Whisper.cpp...")
    try:
        transcript = transcribe_with_whisper(AUDIO_FILE)
        print(f"📝 You said: {transcript}")
        
        if transcript.strip():
            # Process with AI assistant
            print("🤖 Processing with AI...")
            response = assistant.process_input(transcript)
            print(f"🧠 MemoryMate: {response}")
            
            # Speak response
            print("🔊 Speaking response...")
            speak_text(response)
        else:
            print("⚠️ No speech detected. Please try again.")
            
    except Exception as e:
        print(f"❌ Transcription failed: {e}")
        print("💡 Make sure Whisper.cpp is properly set up")


def text_input_mode(assistant):
    """Handle text input mode"""
    print("\n📝 Text Input Mode")
    print("💡 Type your request (e.g., 'Remind me to call mom tomorrow')")
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'back']:
            break
        
        if user_input:
            print("🤖 Processing...")
            response = assistant.process_input(user_input)
            print(f"🧠 MemoryMate: {response}")
            
            # Ask if user wants to hear it spoken
            speak_choice = input("🔊 Would you like me to speak this? (y/n): ").lower()
            if speak_choice in ['y', 'yes']:
                speak_text(response)


def view_tasks(assistant):
    """Display all tasks"""
    print("\n📊 Your Tasks")
    print("=" * 50)
    
    all_tasks = assistant.task_manager.get_all_tasks()
    
    if not all_tasks:
        print("🎉 No tasks found! You're all caught up.")
        return
    
    # Group by priority
    urgent_tasks = [t for t in all_tasks if t.priority == Priority.URGENT_IMPORTANT and t.status != TaskStatus.COMPLETED]
    important_tasks = [t for t in all_tasks if t.priority == Priority.IMPORTANT_NOT_URGENT and t.status != TaskStatus.COMPLETED]
    optional_tasks = [t for t in all_tasks if t.priority == Priority.OPTIONAL and t.status != TaskStatus.COMPLETED]
    completed_tasks = [t for t in all_tasks if t.status == TaskStatus.COMPLETED]
    
    # Display urgent tasks
    if urgent_tasks:
        print("\n🔴 URGENT & IMPORTANT:")
        for i, task in enumerate(urgent_tasks, 1):
            status_emoji = "✅" if task.status == TaskStatus.COMPLETED else "⏳" if task.status == TaskStatus.IN_PROGRESS else "📝"
            print(f"  {i}. {status_emoji} {task.title}")
            if task.due_date:
                print(f"     📅 Due: {task.due_date}")
            if task.tags:
                print(f"     🏷️  Tags: {', '.join(task.tags)}")
    
    # Display important tasks
    if important_tasks:
        print("\n🟡 IMPORTANT:")
        for i, task in enumerate(important_tasks, 1):
            status_emoji = "✅" if task.status == TaskStatus.COMPLETED else "⏳" if task.status == TaskStatus.IN_PROGRESS else "📝"
            print(f"  {i}. {status_emoji} {task.title}")
            if task.due_date:
                print(f"     📅 Due: {task.due_date}")
            if task.tags:
                print(f"     🏷️  Tags: {', '.join(task.tags)}")
    
    # Display optional tasks
    if optional_tasks:
        print("\n🟢 OPTIONAL:")
        for i, task in enumerate(optional_tasks, 1):
            status_emoji = "✅" if task.status == TaskStatus.COMPLETED else "⏳" if task.status == TaskStatus.IN_PROGRESS else "📝"
            print(f"  {i}. {status_emoji} {task.title}")
            if task.due_date:
                print(f"     📅 Due: {task.due_date}")
            if task.tags:
                print(f"     🏷️  Tags: {', '.join(task.tags)}")
    
    # Display completed tasks
    if completed_tasks:
        print(f"\n✅ COMPLETED ({len(completed_tasks)}):")
        for i, task in enumerate(completed_tasks[-5:], 1):  # Show last 5
            print(f"  {i}. {task.title}")
    
    print("\n" + "=" * 50)


def focus_mode(assistant):
    """Focus mode for working on one task"""
    print("\n🎯 Focus Mode")
    print("💡 Focus on one task at a time for maximum productivity")
    
    # Get current focus task
    all_tasks = assistant.task_manager.get_all_tasks()
    focus_tasks = [t for t in all_tasks if t.status == TaskStatus.IN_PROGRESS]
    
    if not focus_tasks:
        print("📋 No tasks are currently in progress.")
        
        # Show available tasks to start
        pending_tasks = [t for t in all_tasks if t.status == TaskStatus.PENDING]
        if pending_tasks:
            print("\n🚀 Available tasks to start:")
            for i, task in enumerate(pending_tasks[:5], 1):
                print(f"  {i}. {task.title}")
            
            choice = input("\n🎯 Which task would you like to focus on? (number or 'back'): ")
            if choice.lower() == 'back':
                return
            
            try:
                task_num = int(choice) - 1
                if 0 <= task_num < len(pending_tasks):
                    selected_task = pending_tasks[task_num]
                    selected_task.status = TaskStatus.IN_PROGRESS
                    selected_task.updated_at = time.strftime('%Y-%m-%d %H:%M:%S')
                    assistant.task_manager.update_task(selected_task)
                    print(f"🎯 Now focusing on: {selected_task.title}")
                    focus_tasks = [selected_task]
                else:
                    print("❌ Invalid task number")
                    return
            except ValueError:
                print("❌ Please enter a valid number")
                return
        else:
            print("📝 No pending tasks. Add some tasks first!")
            return
    
    # Focus on the first in-progress task
    focus_task = focus_tasks[0]
    
    print(f"\n🎯 Current Focus: {focus_task.title}")
    if focus_task.description:
        print(f"📝 Description: {focus_task.description}")
    if focus_task.due_date:
        print(f"📅 Due: {focus_task.due_date}")
    print(f"🔴 Priority: {focus_task.priority.value.replace('_', ' ').title()}")
    
    print("\n⏰ Focus Session Options:")
    print("1. 🍅 Start 25-minute Pomodoro")
    print("2. ☕ Take a 5-minute break")
    print("3. ✅ Mark task as complete")
    print("4. ⏸️ Snooze task (1 hour)")
    print("5. 🔄 Switch to different task")
    print("6. 🚪 Exit focus mode")
    
    while True:
        choice = input("\n🎯 Choose an option (1-6): ")
        
        if choice == '1':
            print("🍅 Starting 25-minute Pomodoro session...")
            print("⏰ Focus on your task. I'll notify you when time's up.")
            time.sleep(25 * 60)  # 25 minutes
            speak_text("Time's up! Take a break or continue working.")
            print("⏰ Pomodoro session complete!")
            
        elif choice == '2':
            print("☕ Taking a 5-minute break...")
            print("🛌 Relax and recharge. I'll notify you when break is over.")
            time.sleep(5 * 60)  # 5 minutes
            speak_text("Break time is over! Let's get back to work.")
            print("☕ Break complete!")
            
        elif choice == '3':
            focus_task.status = TaskStatus.COMPLETED
            focus_task.updated_at = time.strftime('%Y-%m-%d %H:%M:%S')
            assistant.task_manager.update_task(focus_task)
            print("✅ Task completed! Great job!")
            speak_text("Congratulations! Task completed successfully.")
            break
            
        elif choice == '4':
            print("⏸️ Task snoozed for 1 hour")
            # Add snooze logic here
            break
            
        elif choice == '5':
            print("🔄 Switching tasks...")
            break
            
        elif choice == '6':
            print("🚪 Exiting focus mode...")
            break
            
        else:
            print("❌ Invalid choice. Please select 1-6.")


def search_tasks(assistant):
    """Search for specific tasks"""
    print("\n🔍 Search Tasks")
    print("💡 Search by title, description, or tags")
    
    query = input("🔍 What are you looking for? ").strip()
    
    if not query:
        print("❌ Please enter a search term")
        return
    
    print(f"🔍 Searching for: {query}")
    tasks = assistant.task_manager.search_tasks(query)
    
    if not tasks:
        print(f"❌ No tasks found matching '{query}'")
        return
    
    print(f"\n✅ Found {len(tasks)} matching tasks:")
    for i, task in enumerate(tasks, 1):
        priority_emoji = "🔴" if task.priority == Priority.URGENT_IMPORTANT else "🟡" if task.priority == Priority.IMPORTANT_NOT_URGENT else "🟢"
        status_emoji = "✅" if task.status == TaskStatus.COMPLETED else "⏳" if task.status == TaskStatus.IN_PROGRESS else "📝"
        
        print(f"\n{i}. {priority_emoji} {status_emoji} {task.title}")
        if task.description:
            print(f"   📝 {task.description}")
        if task.due_date:
            print(f"   📅 Due: {task.due_date}")
        if task.tags:
            print(f"   🏷️  Tags: {', '.join(task.tags)}")


def daily_summary(assistant):
    """Show daily summary"""
    print("\n📅 Daily Summary")
    print("=" * 50)
    
    summary = assistant.get_daily_summary()
    print(summary)
    
    print("\n" + "=" * 50)


def chat_mode(assistant):
    """Interactive chat mode"""
    print("\n💬 Chat Mode")
    print("💡 Chat naturally with your AI assistant. Type 'exit' to return to menu.")
    print("🤖 I can help with tasks, answer questions, and more!")
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'back']:
            print("🚪 Returning to main menu...")
            break
        
        if user_input:
            print("🤖 Processing...")
            response = assistant.process_input(user_input)
            print(f"🧠 MemoryMate: {response}")
            
            # Ask if user wants to hear it spoken
            speak_choice = input("🔊 Speak response? (y/n): ").lower()
            if speak_choice in ['y', 'yes']:
                speak_text(response)


def help_section():
    """Show help information"""
    print("""
❓ MemoryMate Help
==================

🧠 What is MemoryMate?
MemoryMate is your offline AI productivity assistant that helps you:
• Capture and organize tasks using natural language
• Prioritize tasks automatically
• Remember your commitments and preferences
• Work efficiently with voice and text input

🎯 How to Use:

1. 🎤 Voice Input:
   • Speak naturally: "Remind me to call mom tomorrow"
   • I'll transcribe and create a structured task

2. 📝 Text Input:
   • Type your requests: "Add task: Finish report by Friday"
   • I'll parse and organize automatically

3. 📊 Task Management:
   • View all your tasks organized by priority
   • Mark tasks as complete, in progress, or snooze them
   • Search for specific tasks

4. 🎯 Focus Mode:
   • Work on one task at a time
   • Use Pomodoro timer for productivity
   • Get AI motivation and tips

5. 💬 Chat Mode:
   • Ask questions: "What's on my plate today?"
   • Get daily summaries and insights
   • Natural conversation with AI

🔧 Commands & Examples:
• "Add task: Buy groceries tomorrow"
• "Show my urgent tasks"
• "Mark task 1 as done"
• "What did I promise Rohan last week?"
• "Search for study tasks"
• "Give me my daily summary"

💡 Tips:
• Be specific with due dates and priorities
• Use natural language - no need for special syntax
• I'll remember your preferences over time
• Voice input works best in quiet environments

🚀 Advanced Features:
• AI-powered task prioritization
• Semantic memory search
• Automatic task categorization
• Focus mode with productivity tools

Need more help? Just ask me anything!
    """)


def main():
    """Main MemoryMate application"""
    print_banner()
    
    # Initialize AI assistant
    try:
        print("🤖 Initializing MemoryMate...")
        assistant = MemoryMateAssistant()
        print("✅ MemoryMate ready!")
    except Exception as e:
        print(f"❌ Failed to initialize MemoryMate: {e}")
        print("💡 Please check your setup and try again")
        return
    
    # Main application loop
    while True:
        try:
            print_menu()
            choice = input().strip()
            
            if choice == '1':
                voice_input_mode(assistant)
            elif choice == '2':
                text_input_mode(assistant)
            elif choice == '3':
                view_tasks(assistant)
            elif choice == '4':
                focus_mode(assistant)
            elif choice == '5':
                search_tasks(assistant)
            elif choice == '6':
                daily_summary(assistant)
            elif choice == '7':
                chat_mode(assistant)
            elif choice == '8':
                help_section()
            elif choice == '9':
                print("\n👋 Thank you for using MemoryMate!")
                print("🧠 Stay productive and organized!")
                break
            else:
                print("❌ Invalid choice. Please select 1-9.")
            
            input("\n📱 Press Enter to continue...")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for using MemoryMate!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            print("💡 Please try again or check your setup")
            input("Press Enter to continue...")
    
    # Cleanup
    try:
        assistant.close()
    except:
        pass


if __name__ == "__main__":
    main()
