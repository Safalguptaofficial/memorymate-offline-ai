import streamlit as st
import time
import json
from datetime import datetime
import pandas as pd
from ai_assistant import MemoryMateAssistant
from task_manager import Task, Priority, TaskStatus
from tts import speak_text
import plotly.express as px
import plotly.graph_objects as go


# Page configuration
st.set_page_config(
    page_title="MemoryMate - AI Productivity Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .task-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
    }
    .urgent-task {
        border-left-color: #d62728;
        background-color: #fff5f5;
    }
    .important-task {
        border-left-color: #ff7f0e;
        background-color: #fffbf0;
    }
    .optional-task {
        border-left-color: #2ca02c;
        background-color: #f0fff4;
    }
    .status-badge {
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .status-pending { background-color: #ffd700; color: #000; }
    .status-in-progress { background-color: #87ceeb; color: #000; }
    .status-completed { background-color: #90ee90; color: #000; }
    .priority-badge {
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
        margin-left: 0.5rem;
    }
    .priority-urgent { background-color: #ff6b6b; color: white; }
    .priority-important { background-color: #ffa726; color: white; }
    .priority-optional { background-color: #66bb6a; color: white; }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'assistant' not in st.session_state:
        st.session_state.assistant = MemoryMateAssistant()
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'current_view' not in st.session_state:
        st.session_state.current_view = "dashboard"
    if 'voice_input' not in st.session_state:
        st.session_state.voice_input = ""


def get_priority_color(priority):
    """Get color for priority level"""
    if priority == Priority.URGENT_IMPORTANT:
        return "#d62728"
    elif priority == Priority.IMPORTANT_NOT_URGENT:
        return "#ff7f0e"
    else:
        return "#2ca02c"


def get_priority_emoji(priority):
    """Get emoji for priority level"""
    if priority == Priority.URGENT_IMPORTANT:
        return "🔴"
    elif priority == Priority.IMPORTANT_NOT_URGENT:
        return "🟡"
    else:
        return "🟢"


def get_status_emoji(status):
    """Get emoji for task status"""
    if status == TaskStatus.COMPLETED:
        return "✅"
    elif status == TaskStatus.IN_PROGRESS:
        return "⏳"
    else:
        return "📝"


def render_task_card(task, index):
    """Render a single task card"""
    priority_class = f"priority-{task.priority.value.replace('_', '-')}"
    status_class = f"status-{task.status.value.replace('_', '-')}"
    
    # Determine card class based on priority
    card_class = "task-card"
    if task.priority == Priority.URGENT_IMPORTANT:
        card_class += " urgent-task"
    elif task.priority == Priority.IMPORTANT_NOT_URGENT:
        card_class += " important-task"
    else:
        card_class += " optional-task"
    
    with st.container():
        st.markdown(f"""
        <div class="{card_class}">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="margin: 0;">{get_priority_emoji(task.priority)} {get_status_emoji(task.status)} {task.title}</h4>
                <div>
                    <span class="priority-badge {priority_class}">{task.priority.value.replace('_', ' ').title()}</span>
                    <span class="status-badge {status_class}">{task.status.value.replace('_', ' ').title()}</span>
                </div>
            </div>
            {f'<p style="margin: 0.5rem 0; color: #666;">{task.description}</p>' if task.description else ''}
            {f'<p style="margin: 0.5rem 0; color: #666;"><strong>Due:</strong> {task.due_date}</p>' if task.due_date else ''}
            {f'<p style="margin: 0.5rem 0; color: #666;"><strong>Tags:</strong> {", ".join(task.tags)}</p>' if task.tags else ''}
            {f'<p style="margin: 0.5rem 0; color: #666;"><strong>AI Notes:</strong> {task.ai_notes}</p>' if task.ai_notes else ''}
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button(f"Complete", key=f"complete_{index}"):
                task.status = TaskStatus.COMPLETED
                task.updated_at = datetime.now().isoformat()
                st.session_state.assistant.task_manager.update_task(task)
                st.rerun()
        
        with col2:
            if st.button(f"Start", key=f"start_{index}"):
                task.status = TaskStatus.IN_PROGRESS
                task.updated_at = datetime.now().isoformat()
                st.session_state.assistant.task_manager.update_task(task)
                st.rerun()
        
        with col3:
            if st.button(f"Edit", key=f"edit_{index}"):
                st.session_state.editing_task = task
                st.session_state.current_view = "edit_task"
                st.rerun()
        
        with col4:
            if st.button(f"Delete", key=f"delete_{index}"):
                st.session_state.assistant.task_manager.delete_task(task.id)
                st.rerun()


def render_dashboard():
    """Render the main dashboard"""
    st.markdown('<h1 class="main-header">🧠 MemoryMate</h1>', unsafe_allow_html=True)
    st.markdown("### Your AI Productivity Assistant")
    
    # Quick stats
    all_tasks = st.session_state.assistant.task_manager.get_all_tasks()
    pending_tasks = [t for t in all_tasks if t.status == TaskStatus.PENDING]
    completed_tasks = [t for t in all_tasks if t.status == TaskStatus.COMPLETED]
    urgent_tasks = [t for t in all_tasks if t.priority == Priority.URGENT_IMPORTANT and t.status != TaskStatus.COMPLETED]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Tasks", len(all_tasks))
    with col2:
        st.metric("Pending", len(pending_tasks))
    with col3:
        st.metric("Completed", len(completed_tasks))
    with col4:
        st.metric("Urgent", len(urgent_tasks))
    
    # Priority distribution chart
    if all_tasks:
        priority_counts = {}
        for task in all_tasks:
            priority = task.priority.value.replace('_', ' ').title()
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        fig = px.pie(
            values=list(priority_counts.values()),
            names=list(priority_counts.keys()),
            title="Task Priority Distribution",
            color_discrete_map={
                "Urgent Important": "#d62728",
                "Important Not Urgent": "#ff7f0e",
                "Optional": "#2ca02c"
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Quick add task
    st.markdown("### 🚀 Quick Add Task")
    with st.form("quick_add_task"):
        task_title = st.text_input("Task Title")
        task_description = st.text_area("Description (optional)")
        task_due_date = st.date_input("Due Date (optional)")
        task_priority = st.selectbox(
            "Priority",
            [Priority.URGENT_IMPORTANT, Priority.IMPORTANT_NOT_URGENT, Priority.OPTIONAL],
            format_func=lambda x: x.value.replace('_', ' ').title()
        )
        task_tags = st.text_input("Tags (comma-separated)")
        
        if st.form_submit_button("Add Task"):
            if task_title:
                from task_manager import AITaskParser
                task = Task(
                    id=None,
                    title=task_title,
                    description=task_description,
                    due_date=task_due_date.strftime('%Y-%m-%d') if task_due_date else None,
                    priority=task_priority,
                    status=TaskStatus.PENDING,
                    tags=[tag.strip() for tag in task_tags.split(',') if tag.strip()] if task_tags else [],
                    created_at=datetime.now().isoformat(),
                    updated_at=datetime.now().isoformat()
                )
                st.session_state.assistant.task_manager.add_task(task)
                st.success("Task added successfully!")
                st.rerun()
    
    # Task lists
    st.markdown("### 📋 Your Tasks")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        priority_filter = st.selectbox(
            "Filter by Priority",
            ["All", "Urgent & Important", "Important", "Optional"],
            key="priority_filter"
        )
    with col2:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "Pending", "In Progress", "Completed"],
            key="status_filter"
        )
    with col3:
        search_query = st.text_input("Search tasks", key="search_filter")
    
    # Apply filters
    filtered_tasks = all_tasks
    if priority_filter != "All":
        priority_map = {
            "Urgent & Important": Priority.URGENT_IMPORTANT,
            "Important": Priority.IMPORTANT_NOT_URGENT,
            "Optional": Priority.OPTIONAL
        }
        filtered_tasks = [t for t in filtered_tasks if t.priority == priority_map[priority_filter]]
    
    if status_filter != "All":
        status_map = {
            "Pending": TaskStatus.PENDING,
            "In Progress": TaskStatus.IN_PROGRESS,
            "Completed": TaskStatus.COMPLETED
        }
        filtered_tasks = [t for t in filtered_tasks if t.status == status_map[status_filter]]
    
    if search_query:
        filtered_tasks = [t for t in filtered_tasks if search_query.lower() in t.title.lower() or 
                         (t.description and search_query.lower() in t.description.lower())]
    
    # Display tasks
    if filtered_tasks:
        for i, task in enumerate(filtered_tasks):
            render_task_card(task, i)
    else:
        st.info("No tasks found matching your filters.")


def render_chat():
    """Render the AI chat interface"""
    st.markdown('<h1 class="main-header">💬 AI Chat</h1>', unsafe_allow_html=True)
    st.markdown("### Chat with your AI productivity assistant")
    
    # Chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>You:</strong> {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <strong>MemoryMate:</strong> {message["content"]}
            </div>
            """, unsafe_allow_html=True)
    
    # Voice input section
    st.markdown("### 🎤 Voice Input")
    col1, col2 = st.columns([3, 1])
    with col1:
        voice_input = st.text_input(
            "Or type your message here:",
            value=st.session_state.voice_input,
            key="chat_input",
            placeholder="e.g., 'Remind me to call mom tomorrow' or 'What's on my plate today?'"
        )
    with col2:
        if st.button("🎤 Record Voice", key="record_voice"):
            st.info("Voice recording functionality will be integrated here. For now, please type your message.")
    
    # Send button
    if st.button("Send", key="send_chat"):
        if voice_input.strip():
            # Process with AI assistant
            response = st.session_state.assistant.process_input(voice_input.strip())
            
            # Add to chat history
            st.session_state.chat_history.append({"role": "user", "content": voice_input.strip()})
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            
            # Clear input
            st.session_state.voice_input = ""
            st.rerun()
    
    # Quick action buttons
    st.markdown("### ⚡ Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📋 Show My Tasks"):
            response = st.session_state.assistant.process_input("What's on my plate today?")
            st.session_state.chat_history.append({"role": "user", "content": "What's on my plate today?"})
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col2:
        if st.button("📅 Daily Summary"):
            response = st.session_state.assistant.get_daily_summary()
            st.session_state.chat_history.append({"role": "user", "content": "Show me my daily summary"})
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col3:
        if st.button("🔍 Search Tasks"):
            search_query = st.text_input("What are you looking for?", key="search_chat")
            if search_query:
                response = st.session_state.assistant.process_input(f"Search for {search_query}")
                st.session_state.chat_history.append({"role": "user", "content": f"Search for {search_query}"})
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()
    
    with col4:
        if st.button("❓ Help"):
            response = st.session_state.assistant.process_input("What can you do?")
            st.session_state.chat_history.append({"role": "user", "content": "What can you do?"})
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()


def render_focus_mode():
    """Render the focus mode interface"""
    st.markdown('<h1 class="main-header">🎯 Focus Mode</h1>', unsafe_allow_html=True)
    st.markdown("### Stay focused on one task at a time")
    
    # Get current focus task
    all_tasks = st.session_state.assistant.task_manager.get_all_tasks()
    focus_tasks = [t for t in all_tasks if t.status == TaskStatus.IN_PROGRESS]
    
    if not focus_tasks:
        st.info("No tasks are currently in progress. Start a task to enter focus mode.")
        
        # Show available tasks to start
        pending_tasks = [t for t in all_tasks if t.status == TaskStatus.PENDING]
        if pending_tasks:
            st.markdown("### Available tasks to start:")
            for i, task in enumerate(pending_tasks[:5]):
                if st.button(f"Start: {task.title}", key=f"start_focus_{i}"):
                    task.status = TaskStatus.IN_PROGRESS
                    task.updated_at = datetime.now().isoformat()
                    st.session_state.assistant.task_manager.update_task(task)
                    st.rerun()
        return
    
    # Focus on the first in-progress task
    focus_task = focus_tasks[0]
    
    # Task display
    st.markdown(f"""
    <div class="task-card urgent-task">
        <h2>🎯 Current Focus: {focus_task.title}</h2>
        {f'<p><strong>Description:</strong> {focus_task.description}</p>' if focus_task.description else ''}
        {f'<p><strong>Due:</strong> {focus_task.due_date}</p>' if focus_task.due_date else ''}
        <p><strong>Priority:</strong> {focus_task.priority.value.replace('_', ' ').title()}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Pomodoro timer
    st.markdown("### ⏰ Pomodoro Timer")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🍅 Start 25min"):
            st.session_state.pomodoro_start = time.time()
            st.session_state.pomodoro_duration = 25 * 60  # 25 minutes
            st.rerun()
    
    with col2:
        if st.button("☕ Short Break (5min)"):
            st.session_state.pomodoro_start = time.time()
            st.session_state.pomodoro_duration = 5 * 60  # 5 minutes
            st.rerun()
    
    with col3:
        if st.button("🛌 Long Break (15min)"):
            st.session_state.pomodoro_start = time.time()
            st.session_state.pomodoro_duration = 15 * 60  # 15 minutes
            st.rerun()
    
    # Timer display
    if 'pomodoro_start' in st.session_state and 'pomodoro_duration' in st.session_state:
        elapsed = time.time() - st.session_state.pomodoro_start
        remaining = max(0, st.session_state.pomodoro_duration - elapsed)
        
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        
        st.markdown(f"### ⏱️ Time Remaining: {minutes:02d}:{seconds:02d}")
        
        # Progress bar
        progress = 1 - (remaining / st.session_state.pomodoro_duration)
        st.progress(progress)
        
        if remaining <= 0:
            st.success("⏰ Time's up! Take a break or continue working.")
            # Play notification sound (TTS)
            speak_text("Time's up! Take a break or continue working.")
    
    # Task actions
    st.markdown("### 🎯 Task Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✅ Mark Complete"):
            focus_task.status = TaskStatus.COMPLETED
            focus_task.updated_at = datetime.now().isoformat()
            st.session_state.assistant.task_manager.update_task(focus_task)
            st.success("Task completed! Great job!")
            st.rerun()
    
    with col2:
        if st.button("⏸️ Snooze (1 hour)"):
            # Add snooze logic here
            st.info("Task snoozed for 1 hour")
    
    with col3:
        if st.button("🔄 Switch Task"):
            st.session_state.current_view = "dashboard"
            st.rerun()
    
    # AI motivation
    st.markdown("### 🤖 AI Motivation")
    motivation_messages = [
        "You're doing great! Stay focused and you'll get this done.",
        "Remember why this task is important to you.",
        "Take it one step at a time. You've got this!",
        "A little progress each day adds up to big results.",
        "Focus on the process, not just the outcome."
    ]
    
    import random
    motivation = random.choice(motivation_messages)
    st.info(f"💡 {motivation}")


def render_settings():
    """Render the settings page"""
    st.markdown('<h1 class="main-header">⚙️ Settings</h1>', unsafe_allow_html=True)
    
    st.markdown("### 🎙️ Voice Settings")
    col1, col2 = st.columns(2)
    
    with col1:
        speech_rate = st.slider("Speech Rate", 100, 300, 180, help="Words per minute")
        if st.button("Apply Speech Rate"):
            from tts import tts_engine
            tts_engine.change_rate(speech_rate)
            st.success("Speech rate updated!")
    
    with col2:
        volume = st.slider("Volume", 0.0, 1.0, 0.9, help="TTS volume level")
        if st.button("Apply Volume"):
            from tts import tts_engine
            tts_engine.change_volume(volume)
            st.success("Volume updated!")
    
    st.markdown("### 🗄️ Data Management")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Export Tasks"):
            all_tasks = st.session_state.assistant.task_manager.get_all_tasks()
            if all_tasks:
                # Convert tasks to exportable format
                export_data = []
                for task in all_tasks:
                    export_data.append({
                        'title': task.title,
                        'description': task.description,
                        'due_date': task.due_date,
                        'priority': task.priority.value,
                        'status': task.status.value,
                        'tags': ', '.join(task.tags) if task.tags else '',
                        'created_at': task.created_at,
                        'updated_at': task.updated_at
                    })
                
                df = pd.DataFrame(export_data)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"memorymate_tasks_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            else:
                st.info("No tasks to export")
    
    with col2:
        if st.button("Clear All Data"):
            if st.checkbox("I understand this will delete all my data"):
                # Clear all data
                st.session_state.assistant.task_manager.conn.execute("DELETE FROM tasks")
                st.session_state.assistant.task_manager.conn.commit()
                st.session_state.assistant.memory_store.conn.execute("DELETE FROM memory")
                st.session_state.assistant.memory_store.conn.commit()
                st.session_state.chat_history = []
                st.success("All data cleared!")
                st.rerun()
    
    st.markdown("### 🔧 System Information")
    st.info(f"""
    **MemoryMate Version:** 1.0.0
    **Database:** SQLite
    **AI Models:** Whisper.cpp + LLaMA.cpp + FAISS
    **Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """)


def main():
    """Main application function"""
    initialize_session_state()
    
    # Sidebar navigation
    st.sidebar.markdown("## 🧠 MemoryMate")
    st.sidebar.markdown("Your AI Productivity Assistant")
    
    # Navigation
    current_view = st.sidebar.selectbox(
        "Navigation",
        ["Dashboard", "AI Chat", "Focus Mode", "Settings"],
        index=["Dashboard", "AI Chat", "Focus Mode", "Settings"].index(st.session_state.current_view)
    )
    
    # Update current view
    if current_view == "Dashboard":
        st.session_state.current_view = "dashboard"
    elif current_view == "AI Chat":
        st.session_state.current_view = "chat"
    elif current_view == "Focus Mode":
        st.session_state.current_view = "focus"
    elif current_view == "Settings":
        st.session_state.current_view = "settings"
    
    # Sidebar quick actions
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚡ Quick Actions")
    
    if st.sidebar.button("📋 Add Quick Task"):
        st.session_state.current_view = "dashboard"
        st.rerun()
    
    if st.sidebar.button("🎯 Start Focus Session"):
        st.session_state.current_view = "focus"
        st.rerun()
    
    if st.sidebar.button("📊 Daily Summary"):
        summary = st.session_state.assistant.get_daily_summary()
        st.sidebar.markdown("### 📊 Daily Summary")
        st.sidebar.markdown(summary)
    
    # Main content area
    if st.session_state.current_view == "dashboard":
        render_dashboard()
    elif st.session_state.current_view == "chat":
        render_chat()
    elif st.session_state.current_view == "focus":
        render_focus_mode()
    elif st.session_state.current_view == "settings":
        render_settings()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "🧠 **MemoryMate** - Offline AI Productivity Assistant | "
        "Built with Whisper.cpp, LLaMA.cpp, and FAISS"
    )


if __name__ == "__main__":
    main()
