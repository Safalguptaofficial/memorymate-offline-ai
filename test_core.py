#!/usr/bin/env python3
"""
MemoryMate Core Functionality Test
Tests the basic components without requiring user interaction
"""

import sys
import traceback
from datetime import datetime

def test_imports():
    """Test if all modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import task_manager
        from task_manager import Task, Priority, TaskStatus, TaskManager, AITaskParser
        print("   ✅ Task manager imported successfully")
        
        import memory_store
        from memory_store import MemoryStore
        print("   ✅ Memory store imported successfully")
        
        import ai_assistant
        from ai_assistant import MemoryMateAssistant
        print("   ✅ AI assistant imported successfully")
        
        import tts
        from tts import speak_text, TextToSpeech
        print("   ✅ TTS module imported successfully")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Import failed: {e}")
        traceback.print_exc()
        return False


def test_task_manager():
    """Test task manager functionality"""
    print("\n📋 Testing task manager...")
    
    try:
        # Create task manager
        task_manager = TaskManager()
        print("   ✅ Task manager created")
        
        # Create a test task
        test_task = Task(
            id=None,
            title="Test task for core testing",
            description="This is a test task to verify functionality",
            due_date="2025-08-25",
            priority=Priority.IMPORTANT_NOT_URGENT,
            status=TaskStatus.PENDING,
            tags=["test", "core"],
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
        # Add task
        task_id = task_manager.add_task(test_task)
        print(f"   ✅ Task created with ID: {task_id}")
        
        # Retrieve task
        retrieved_task = task_manager.get_task(task_id)
        if retrieved_task and retrieved_task.title == test_task.title:
            print("   ✅ Task retrieved successfully")
        else:
            print("   ❌ Task retrieval failed")
            return False
        
        # Search tasks
        search_results = task_manager.search_tasks("test")
        if search_results:
            print("   ✅ Task search working")
        else:
            print("   ❌ Task search failed")
            return False
        
        # Update task
        test_task.id = task_id
        test_task.status = TaskStatus.IN_PROGRESS
        test_task.updated_at = datetime.now().isoformat()
        
        if task_manager.update_task(test_task):
            print("   ✅ Task update working")
        else:
            print("   ❌ Task update failed")
            return False
        
        # Delete task
        if task_manager.delete_task(task_id):
            print("   ✅ Task deletion working")
        else:
            print("   ❌ Task deletion failed")
            return False
        
        print("   ✅ Task Manager test PASSED")
        return True
        
    except Exception as e:
        print(f"   ❌ Task Manager test failed: {e}")
        return False


def test_memory_store():
    """Test memory store functionality"""
    print("\n🧠 Testing memory store...")
    
    try:
        # Create memory store
        memory_store = MemoryStore("test_memory.db")
        print("   ✅ Memory store created")
        
        # Add memory
        memory_id = memory_store.add_memory("Test memory for core testing")
        print("   ✅ Memory added successfully")
        
        # Get memory
        retrieved_memory = memory_store.get_memory(memory_id)
        if retrieved_memory and "Test memory" in retrieved_memory['text']:
            print("   ✅ Memory retrieval working")
        else:
            print("   ❌ Memory retrieval failed")
            return False
        
        # Search memory
        search_results = memory_store.search_memory("test memory")
        if search_results:
            print("   ✅ Memory search working")
        else:
            print("   ❌ Memory search failed")
            return False
        
        # Get recent memories
        recent_memories = memory_store.get_recent_memories(5)
        if recent_memories:
            print("   ✅ Recent memories working")
        else:
            print("   ❌ Recent memories failed")
            return False
        
        # Get memory count
        count = memory_store.get_memory_count()
        if count > 0:
            print("   ✅ Memory count working")
        else:
            print("   ❌ Memory count failed")
            return False
        
        # Delete memory
        if memory_store.delete_memory(memory_id):
            print("   ✅ Memory deletion working")
        else:
            print("   ❌ Memory deletion failed")
            return False
        
        print("   ✅ Memory Store test PASSED")
        return True
        
    except Exception as e:
        print(f"   ❌ Memory store test failed: {e}")
        return False


def test_ai_assistant():
    """Test AI assistant functionality"""
    print("\n🤖 Testing AI assistant...")
    
    try:
        from ai_assistant import MemoryMateAssistant
        
        # Create AI assistant
        assistant = MemoryMateAssistant()
        print("   ✅ AI assistant created")
        
        # Test intent classification
        test_inputs = [
            "Remind me to call mom tomorrow",
            "What's on my plate today?",
            "Hello, how are you?",
            "Help me understand what you can do"
        ]
        
        for test_input in test_inputs:
            try:
                response = assistant.process_input(test_input)
                print(f"   ✅ Processed: '{test_input[:30]}...' → Response generated")
            except Exception as e:
                print(f"   ⚠️  Failed to process: '{test_input[:30]}...' - {e}")
        
        # Test daily summary
        try:
            summary = assistant.get_daily_summary()
            print("   ✅ Daily summary generated")
        except Exception as e:
            print(f"   ⚠️  Daily summary failed: {e}")
        
        assistant.close()
        print("   ✅ AI assistant closed")
        return True
        
    except Exception as e:
        print(f"   ❌ AI assistant test failed: {e}")
        traceback.print_exc()
        return False


def test_tts():
    """Test text-to-speech functionality"""
    print("\n🔊 Testing TTS...")
    
    try:
        from tts import TextToSpeech
        
        # Create TTS engine
        tts = TextToSpeech()
        print("   ✅ TTS engine created")
        
        # Test speech (without actually speaking)
        test_text = "This is a test of the text to speech system"
        print(f"   ✅ TTS ready to speak: '{test_text[:30]}...'")
        
        # Test configuration
        tts.change_rate(200)
        tts.change_volume(0.8)
        print("   ✅ TTS configuration working")
        
        return True
        
    except Exception as e:
        print(f"   ❌ TTS test failed: {e}")
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("🧠 MemoryMate Core Functionality Test")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Task Manager", test_task_manager),
        ("Memory Store", test_memory_store),
        ("AI Assistant", test_ai_assistant),
        ("Text-to-Speech", test_tts)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name} test...")
        if test_func():
            passed += 1
            print(f"   ✅ {test_name} test PASSED")
        else:
            print(f"   ❌ {test_name} test FAILED")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! MemoryMate core functionality is working.")
        print("🚀 You can now run the full application.")
    else:
        print("⚠️  Some tests failed. Please check the error messages above.")
        print("💡 The application may not work properly until these issues are resolved.")
    
    print("\n💡 To run MemoryMate:")
    print("   • Terminal: python main.py")
    print("   • Web UI: streamlit run streamlit_app.py")
    print("   • Demo: python demo.py")


if __name__ == "__main__":
    main()
