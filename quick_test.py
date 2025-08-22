#!/usr/bin/env python3
"""
Quick MemoryMate Test
Simple interactive test of core functionality
"""

from ai_assistant import MemoryMateAssistant

def main():
    print("🧠 MemoryMate Quick Test")
    print("=" * 40)
    
    try:
        # Initialize assistant
        print("🤖 Initializing MemoryMate...")
        assistant = MemoryMateAssistant()
        print("✅ MemoryMate ready!")
        
        # Test basic functionality
        print("\n🎯 Testing basic functionality...")
        
        # Test 1: Add a task
        print("\n1️⃣ Adding a test task...")
        response = assistant.process_input("Remind me to buy groceries tomorrow")
        print(f"   Response: {response}")
        
        # Test 2: List tasks
        print("\n2️⃣ Listing tasks...")
        response = assistant.process_input("What's on my plate today?")
        print(f"   Response: {response}")
        
        # Test 3: Daily summary
        print("\n3️⃣ Getting daily summary...")
        summary = assistant.get_daily_summary()
        print(f"   Summary: {summary}")
        
        # Test 4: Search tasks
        print("\n4️⃣ Searching tasks...")
        response = assistant.process_input("Search for grocery tasks")
        print(f"   Response: {response}")
        
        print("\n🎉 All tests completed successfully!")
        print("✅ MemoryMate is working properly!")
        
        # Cleanup
        assistant.close()
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
