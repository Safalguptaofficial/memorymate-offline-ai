import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from task_manager import TaskManager, AITaskParser, Task, Priority, TaskStatus
from memory_store import MemoryStore
from transcribe_and_respond import generate_llama_response


class MemoryMateAssistant:
    def __init__(self):
        self.task_manager = TaskManager()
        self.memory_store = MemoryStore()
        self.conversation_history = []
        
    def process_input(self, user_input: str) -> str:
        """Process user input and generate appropriate response"""
        # Store in memory
        self.memory_store.add_memory(f"User: {user_input}")
        
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Determine intent and generate response
        intent = self._classify_intent(user_input)
        response = self._handle_intent(intent, user_input)
        
        # Store response in memory
        self.memory_store.add_memory(f"Assistant: {response}")
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return response
    
    def _classify_intent(self, user_input: str) -> str:
        """Classify user intent from input"""
        input_lower = user_input.lower()
        
        # Task management intents
        if any(word in input_lower for word in ['add', 'create', 'new', 'remind', 'task']):
            return 'add_task'
        elif any(word in input_lower for word in ['list', 'show', 'what', 'tasks', 'todo']):
            return 'list_tasks'
        elif any(word in input_lower for word in ['complete', 'done', 'finished', 'mark']):
            return 'complete_task'
        elif any(word in input_lower for word in ['delete', 'remove', 'cancel']):
            return 'delete_task'
        elif any(word in input_lower for word in ['search', 'find', 'look']):
            return 'search_tasks'
        elif any(word in input_lower for word in ['priority', 'urgent', 'important']):
            return 'prioritize_tasks'
        
        # Memory/recall intents
        elif any(word in input_lower for word in ['remember', 'recall', 'what did', 'promised']):
            return 'recall_memory'
        
        # General chat intents
        elif any(word in input_lower for word in ['hello', 'hi', 'hey', 'how are you']):
            return 'greeting'
        elif any(word in input_lower for word in ['help', 'what can you do']):
            return 'help'
        else:
            return 'general_chat'
    
    def _handle_intent(self, intent: str, user_input: str) -> str:
        """Handle specific intent and generate response"""
        if intent == 'add_task':
            return self._handle_add_task(user_input)
        elif intent == 'list_tasks':
            return self._handle_list_tasks(user_input)
        elif intent == 'complete_task':
            return self._handle_complete_task(user_input)
        elif intent == 'delete_task':
            return self._handle_delete_task(user_input)
        elif intent == 'search_tasks':
            return self._handle_search_tasks(user_input)
        elif intent == 'prioritize_tasks':
            return self._handle_prioritize_tasks(user_input)
        elif intent == 'recall_memory':
            return self._handle_recall_memory(user_input)
        elif intent == 'greeting':
            return self._handle_greeting()
        elif intent == 'help':
            return self._handle_help()
        else:
            return self._handle_general_chat(user_input)
    
    def _handle_add_task(self, user_input: str) -> str:
        """Handle adding a new task"""
        try:
            # Parse task from natural language
            task = AITaskParser.parse_task_from_text(user_input)
            
            # Add to task manager
            task_id = self.task_manager.add_task(task)
            
            # Generate AI response
            response = f"I've added the task '{task.title}' to your list. "
            
            if task.due_date:
                response += f"It's due on {task.due_date}. "
            
            if task.priority == Priority.URGENT_IMPORTANT:
                response += "I've marked it as urgent and important. "
            elif task.priority == Priority.IMPORTANT_NOT_URGENT:
                response += "I've marked it as important. "
            
            if task.tags:
                response += f"I've tagged it with: {', '.join(task.tags)}. "
            
            return response
            
        except Exception as e:
            return f"Sorry, I couldn't add that task. Error: {str(e)}"
    
    def _handle_list_tasks(self, user_input: str) -> str:
        """Handle listing tasks"""
        try:
            # Check for specific filters
            if 'urgent' in user_input.lower():
                tasks = self.task_manager.get_tasks_by_priority(Priority.URGENT_IMPORTANT)
                response = "Here are your urgent and important tasks:\n"
            elif 'important' in user_input.lower():
                tasks = self.task_manager.get_tasks_by_priority(Priority.IMPORTANT_NOT_URGENT)
                response = "Here are your important tasks:\n"
            elif 'today' in user_input.lower():
                today = datetime.now().strftime('%Y-%m-%d')
                all_tasks = self.task_manager.get_all_tasks()
                tasks = [t for t in all_tasks if t.due_date == today]
                response = f"Here are your tasks for today ({today}):\n"
            else:
                tasks = self.task_manager.get_all_tasks()
                response = "Here are all your tasks:\n"
            
            if not tasks:
                response += "No tasks found."
            else:
                for i, task in enumerate(tasks[:10], 1):  # Limit to 10 tasks
                    priority_emoji = "🔴" if task.priority == Priority.URGENT_IMPORTANT else "🟡" if task.priority == Priority.IMPORTANT_NOT_URGENT else "🟢"
                    status_emoji = "✅" if task.status == TaskStatus.COMPLETED else "⏳" if task.status == TaskStatus.IN_PROGRESS else "📝"
                    
                    response += f"{i}. {priority_emoji} {status_emoji} {task.title}"
                    if task.due_date:
                        response += f" (Due: {task.due_date})"
                    response += "\n"
                
                if len(tasks) > 10:
                    response += f"... and {len(tasks) - 10} more tasks."
            
            return response
            
        except Exception as e:
            return f"Sorry, I couldn't list your tasks. Error: {str(e)}"
    
    def _handle_complete_task(self, user_input: str) -> str:
        """Handle completing a task"""
        try:
            # Try to find task by number or title
            all_tasks = self.task_manager.get_all_tasks()
            
            # Check if user mentioned a number
            number_match = re.search(r'(\d+)', user_input)
            if number_match:
                task_num = int(number_match.group(1)) - 1
                if 0 <= task_num < len(all_tasks):
                    task = all_tasks[task_num]
                    task.status = TaskStatus.COMPLETED
                    task.updated_at = datetime.now().isoformat()
                    self.task_manager.update_task(task)
                    return f"Great job! I've marked '{task.title}' as completed. 🎉"
            
            # Try to find by title
            for task in all_tasks:
                if task.title.lower() in user_input.lower():
                    task.status = TaskStatus.COMPLETED
                    task.updated_at = datetime.now().isoformat()
                    self.task_manager.update_task(task)
                    return f"Great job! I've marked '{task.title}' as completed. 🎉"
            
            return "I couldn't find that task. Could you be more specific?"
            
        except Exception as e:
            return f"Sorry, I couldn't complete that task. Error: {str(e)}"
    
    def _handle_delete_task(self, user_input: str) -> str:
        """Handle deleting a task"""
        try:
            all_tasks = self.task_manager.get_all_tasks()
            
            # Check if user mentioned a number
            number_match = re.search(r'(\d+)', user_input)
            if number_match:
                task_num = int(number_match.group(1)) - 1
                if 0 <= task_num < len(all_tasks):
                    task = all_tasks[task_num]
                    self.task_manager.delete_task(task.id)
                    return f"I've deleted the task '{task.title}'."
            
            # Try to find by title
            for task in all_tasks:
                if task.title.lower() in user_input.lower():
                    self.task_manager.delete_task(task.id)
                    return f"I've deleted the task '{task.title}'."
            
            return "I couldn't find that task. Could you be more specific?"
            
        except Exception as e:
            return f"Sorry, I couldn't delete that task. Error: {str(e)}"
    
    def _handle_search_tasks(self, user_input: str) -> str:
        """Handle searching tasks"""
        try:
            # Extract search query
            search_terms = ['search', 'find', 'look for', 'show me']
            query = user_input.lower()
            for term in search_terms:
                query = query.replace(term, '').strip()
            
            if not query:
                return "What would you like me to search for?"
            
            tasks = self.task_manager.search_tasks(query)
            
            if not tasks:
                return f"I couldn't find any tasks matching '{query}'."
            
            response = f"Here are tasks matching '{query}':\n"
            for i, task in enumerate(tasks[:5], 1):
                priority_emoji = "🔴" if task.priority == Priority.URGENT_IMPORTANT else "🟡" if task.priority == Priority.IMPORTANT_NOT_URGENT else "🟢"
                response += f"{i}. {priority_emoji} {task.title}"
                if task.due_date:
                    response += f" (Due: {task.due_date})"
                response += "\n"
            
            return response
            
        except Exception as e:
            return f"Sorry, I couldn't search your tasks. Error: {str(e)}"
    
    def _handle_prioritize_tasks(self, user_input: str) -> str:
        """Handle task prioritization"""
        try:
            all_tasks = self.task_manager.get_all_tasks()
            pending_tasks = [t for t in all_tasks if t.status == TaskStatus.PENDING]
            
            if not pending_tasks:
                return "You have no pending tasks to prioritize."
            
            # Simple prioritization logic
            for task in pending_tasks:
                if any(word in task.title.lower() for word in ['urgent', 'asap', 'emergency', 'critical']):
                    task.priority = Priority.URGENT_IMPORTANT
                elif any(word in task.title.lower() for word in ['important', 'priority', 'key']):
                    task.priority = Priority.IMPORTANT_NOT_URGENT
                else:
                    task.priority = Priority.OPTIONAL
                
                task.updated_at = datetime.now().isoformat()
                self.task_manager.update_task(task)
            
            return "I've updated the priorities of your tasks based on their content and urgency."
            
        except Exception as e:
            return f"Sorry, I couldn't prioritize your tasks. Error: {str(e)}"
    
    def _handle_recall_memory(self, user_input: str) -> str:
        """Handle memory recall"""
        try:
            # Search memory for relevant information
            memories = self.memory_store.search_memory(user_input, k=3)
            
            if not memories:
                return "I don't have any specific memories about that. Could you be more specific?"
            
            response = "Here's what I remember:\n"
            for i, memory in enumerate(memories, 1):
                response += f"{i}. {memory}\n"
            
            return response
            
        except Exception as e:
            return f"Sorry, I couldn't recall that memory. Error: {str(e)}"
    
    def _handle_greeting(self) -> str:
        """Handle greetings"""
        greetings = [
            "Hello! I'm MemoryMate, your AI productivity assistant. How can I help you today?",
            "Hi there! Ready to boost your productivity? What would you like to work on?",
            "Hey! I'm here to help you stay organized and productive. What's on your mind?",
            "Greetings! Let's make today productive together. What can I help you with?"
        ]
        return greetings[hash(datetime.now().strftime('%Y-%m-%d')) % len(greetings)]
    
    def _handle_help(self) -> str:
        """Handle help requests"""
        return """I'm MemoryMate, your AI productivity assistant! Here's what I can do:

🎯 **Task Management:**
• Add tasks: "Remind me to call mom tomorrow"
• List tasks: "What's on my plate today?"
• Complete tasks: "Mark task 1 as done"
• Delete tasks: "Remove the meeting task"

🔍 **Search & Recall:**
• Search tasks: "Find my study tasks"
• Memory recall: "What did I promise Rohan?"

📊 **Organization:**
• Priority management: "Show urgent tasks"
• Task categorization: I automatically tag and prioritize

💬 **Natural Language:**
• Just speak naturally: "I need to finish the report by Friday"
• I'll parse it into a structured task

What would you like to try first?"""
    
    def _handle_general_chat(self, user_input: str) -> str:
        """Handle general chat using LLaMA"""
        try:
            # Use LLaMA for general conversation
            response = generate_llama_response(user_input)
            return response
        except Exception as e:
            return f"I'm having trouble processing that. Could you try rephrasing or ask me to help with a specific task?"
    
    def get_daily_summary(self) -> str:
        """Generate a daily summary of tasks and progress"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            all_tasks = self.task_manager.get_all_tasks()
            
            today_tasks = [t for t in all_tasks if t.due_date == today]
            completed_today = [t for t in all_tasks if t.status == TaskStatus.COMPLETED and t.updated_at.startswith(today)]
            urgent_tasks = [t for t in all_tasks if t.priority == Priority.URGENT_IMPORTANT and t.status != TaskStatus.COMPLETED]
            
            summary = f"📅 **Daily Summary for {today}**\n\n"
            
            if today_tasks:
                summary += f"📋 **Due Today ({len(today_tasks)}):**\n"
                for task in today_tasks:
                    summary += f"• {task.title}\n"
                summary += "\n"
            
            if completed_today:
                summary += f"✅ **Completed Today ({len(completed_today)}):**\n"
                for task in completed_today:
                    summary += f"• {task.title}\n"
                summary += "\n"
            
            if urgent_tasks:
                summary += f"🔴 **Urgent & Important ({len(urgent_tasks)}):**\n"
                for task in urgent_tasks:
                    summary += f"• {task.title}"
                    if task.due_date:
                        summary += f" (Due: {task.due_date})"
                    summary += "\n"
            
            if not today_tasks and not completed_today and not urgent_tasks:
                summary += "🎉 Great job! You have no urgent tasks and nothing due today."
            
            return summary
            
        except Exception as e:
            return f"Sorry, I couldn't generate your daily summary. Error: {str(e)}"
    
    def close(self):
        """Clean up resources"""
        self.task_manager.close()
