import streamlit as st
import time
from datetime import datetime, timedelta
import pandas as pd
from ai_assistant import MemoryMateAssistant
from task_manager import Task, Priority, TaskStatus
from tts import speak_text
import plotly.express as px
import plotly.graph_objects as go
import random
import json

# Page configuration
st.set_page_config(
    page_title="🧠 MemoryMate - AI Productivity Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with Kanban board styles
st.markdown("""
<style>
    /* Modern CSS Variables */
    :root {
        --primary-color: #6366f1;
        --primary-dark: #4f46e5;
        --secondary-color: #8b5cf6;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
        --text-primary: #1f2937;
        --text-secondary: #6b7280;
        --bg-primary: #ffffff;
        --bg-secondary: #f9fafb;
        --border-color: #e5e7eb;
        --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
        --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
    }

    /* Dark Mode Variables */
    [data-theme="dark"] {
        --text-primary: #f9fafb;
        --text-secondary: #d1d5db;
        --bg-primary: #111827;
        --bg-secondary: #1f2937;
        --border-color: #374151;
    }

    /* Global Styles */
    .main {
        background: var(--bg-primary);
        color: var(--text-primary);
    }

    .stApp {
        background: var(--bg-primary);
    }

    /* Modern Header */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        animation: fadeInUp 0.8s ease-out;
    }

    /* Kanban Board Styles */
    .kanban-column {
        background: var(--bg-secondary);
        border-radius: 16px;
        padding: 1rem;
        margin: 0.5rem;
        border: 1px solid var(--border-color);
        min-height: 400px;
        box-shadow: var(--shadow-sm);
    }

    .kanban-column-header {
        text-align: center;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        padding: 0.5rem;
        border-radius: 8px;
        color: white;
    }

    .kanban-column.pending .kanban-column-header {
        background: var(--warning-color);
    }

    .kanban-column.in-progress .kanban-column-header {
        background: var(--primary-color);
    }

    .kanban-column.completed .kanban-column-header {
        background: var(--success-color);
    }

    .kanban-task {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-sm);
        cursor: pointer;
        transition: all 0.3s ease;
        animation: slideInUp 0.4s ease-out;
    }

    .kanban-task:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
        border-color: var(--primary-color);
    }

    .kanban-task.urgent {
        border-left: 4px solid var(--danger-color);
    }

    .kanban-task.important {
        border-left: 4px solid var(--warning-color);
    }

    .kanban-task.optional {
        border-left: 4px solid var(--success-color);
    }

    /* Enhanced Onboarding */
    .onboarding-step {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 24px;
        padding: 2rem;
        margin: 1rem 0;
        text-align: center;
        box-shadow: var(--shadow-lg);
        animation: fadeInUp 0.8s ease-out;
    }

    .onboarding-progress {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 0.5rem;
        margin: 1rem 0;
    }

    .onboarding-progress-bar {
        background: white;
        height: 8px;
        border-radius: 4px;
        transition: width 0.5s ease;
    }

    /* Enhanced Gamification */
    .achievement-unlocked {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: var(--shadow-lg);
        animation: bounceIn 0.6s ease-out;
        margin: 1rem 0;
    }

    .streak-milestone {
        background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%);
        color: white;
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: var(--shadow-lg);
        animation: pulse 2s infinite;
    }

    /* Enhanced Voice Features */
    .voice-recording {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border-radius: 50px;
        padding: 1.5rem 2rem;
        text-align: center;
        box-shadow: var(--shadow-lg);
        animation: pulse 2s infinite;
        margin: 2rem 0;
    }

    .voice-waveform {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 4px;
        margin: 1rem 0;
    }

    .voice-bar {
        width: 4px;
        background: white;
        border-radius: 2px;
        animation: voiceWave 1.5s ease-in-out infinite;
    }

    .voice-bar:nth-child(1) { animation-delay: 0s; height: 20px; }
    .voice-bar:nth-child(2) { animation-delay: 0.1s; height: 30px; }
    .voice-bar:nth-child(3) { animation-delay: 0.2s; height: 25px; }
    .voice-bar:nth-child(4) { animation-delay: 0.3s; height: 35px; }
    .voice-bar:nth-child(5) { animation-delay: 0.4s; height: 20px; }

    @keyframes voiceWave {
        0%, 100% { transform: scaleY(1); }
        50% { transform: scaleY(1.5); }
    }

    /* Enhanced Animations */
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
    }

    @keyframes bounceIn {
        0% {
            opacity: 0;
            transform: scale(0.3);
        }
        50% {
            opacity: 1;
            transform: scale(1.05);
        }
        70% {
            transform: scale(0.9);
        }
        100% {
            opacity: 1;
            transform: scale(1);
        }
    }

    /* Rest of existing CSS styles... */
    .task-card {
        background: var(--bg-secondary);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-sm);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: slideInLeft 0.6s ease-out;
    }

    .task-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
        border-color: var(--primary-color);
    }

    .urgent-task {
        border-left: 6px solid var(--danger-color);
        background: linear-gradient(135deg, #fef2f2, var(--bg-secondary));
    }

    .important-task {
        border-left: 6px solid var(--warning-color);
        background: linear-gradient(135deg, #fffbeb, var(--bg-secondary));
    }

    .optional-task {
        border-left: 6px solid var(--success-color);
        background: linear-gradient(135deg, #f0fdf4, var(--bg-secondary));
    }

    /* Status Badges */
    .status-badge {
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .status-pending { 
        background: linear-gradient(135deg, #fef3c7, #fbbf24);
        color: #92400e;
    }
    
    .status-in-progress { 
        background: linear-gradient(135deg, #dbeafe, #3b82f6);
        color: #1e40af;
    }
    
    .status-completed { 
        background: linear-gradient(135deg, #d1fae5, #10b981);
        color: #065f46;
    }

    /* Priority Badges */
    .priority-badge {
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
        margin-left: 0.5rem;
    }

    .priority-urgent { 
        background: linear-gradient(135deg, #fecaca, #ef4444);
        color: white;
        box-shadow: 0 4px 14px 0 rgba(239, 68, 68, 0.4);
    }
    
    .priority-important { 
        background: linear-gradient(135deg, #fed7aa, #f59e0b);
        color: white;
        box-shadow: 0 4px 14px 0 rgba(245, 158, 11, 0.4);
    }
    
    .priority-optional { 
        background: linear-gradient(135deg, #bbf7d0, #10b981);
        color: white;
        box-shadow: 0 4px 14px 0 rgba(16, 185, 129, 0.4);
    }

    /* Gamification Elements */
    .streak-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        box-shadow: var(--shadow-lg);
        animation: pulse 2s infinite;
    }

    .productivity-score {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        box-shadow: var(--shadow-lg);
    }

    .badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
        animation: bounceIn 0.6s ease-out;
    }

    /* Onboarding Elements */
    .onboarding-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 24px;
        padding: 3rem;
        text-align: center;
        box-shadow: var(--shadow-lg);
        margin: 2rem 0;
    }

    .motivational-quote {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        box-shadow: var(--shadow-lg);
        margin: 2rem 0;
        font-style: italic;
        font-size: 1.2rem;
    }

    /* AI Coach Mode */
    .ai-coach-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: var(--shadow-lg);
        margin: 2rem 0;
    }

    /* Voice Input Button */
    .voice-btn {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: 50px;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-md);
        animation: pulse 2s infinite;
    }

    .voice-btn:hover {
        transform: scale(1.05);
        box-shadow: var(--shadow-lg);
    }

    /* Modern Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-sm);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }

    /* Sidebar Styling */
    .css-1d391kg {
        background: var(--bg-secondary);
    }

    /* Metrics Styling */
    .metric-container {
        background: var(--bg-secondary);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-sm);
        transition: all 0.3s ease;
    }

    .metric-container:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state with enhanced features"""
    if 'assistant' not in st.session_state:
        st.session_state.assistant = MemoryMateAssistant()
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'theme' not in st.session_state:
        st.session_state.theme = "light"
    if 'onboarding_complete' not in st.session_state:
        st.session_state.onboarding_complete = False
    if 'onboarding_step' not in st.session_state:
        st.session_state.onboarding_step = 0
    if 'streak_count' not in st.session_state:
        st.session_state.streak_count = 0
    if 'productivity_score' not in st.session_state:
        st.session_state.productivity_score = 85
    if 'badges' not in st.session_state:
        st.session_state.badges = ["🚀 First Task", "🎯 Focus Master"]
    if 'last_completion_date' not in st.session_state:
        st.session_state.last_completion_date = None
    if 'achievements' not in st.session_state:
        st.session_state.achievements = []
    if 'view_mode' not in st.session_state:
        st.session_state.view_mode = "list"  # "list" or "kanban"
    if 'page' not in st.session_state:
        st.session_state.page = "Dashboard" # Default page


def get_motivational_quote():
    """Get a random motivational quote"""
    quotes = [
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Productivity is never an accident. It is always the result of a commitment to excellence. - Paul J. Meyer",
        "The future depends on what you do today. - Mahatma Gandhi",
        "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
        "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
        "The way to get started is to quit talking and begin doing. - Walt Disney",
        "It always seems impossible until it's done. - Nelson Mandela",
        "The only limit to our realization of tomorrow will be our doubts of today. - Franklin D. Roosevelt",
        "The best way to predict the future is to create it. - Peter Drucker",
        "Excellence is not a skill. It's an attitude. - Ralph Marston"
    ]
    return random.choice(quotes)


def render_enhanced_onboarding():
    """Render enhanced onboarding experience with progress tracking"""
    if not st.session_state.onboarding_complete:
        onboarding_steps = [
            {
                "title": "🎉 Welcome to MemoryMate!",
                "description": "Your AI-powered productivity companion that works 100% offline",
                "features": ["🎤 Voice-powered task creation", "🧠 AI task prioritization", "🔒 100% private", "🎯 Focus mode", "🏆 Gamification"]
            },
            {
                "title": "🔒 Privacy First",
                "description": "Your data never leaves your device",
                "features": ["No internet required", "No data collection", "No cloud storage", "Complete privacy", "Local AI processing"]
            },
            {
                "title": "🤖 AI-Powered",
                "description": "Intelligent task management with offline AI",
                "features": ["Natural language processing", "Smart prioritization", "Context awareness", "Memory system", "Voice interaction"]
            },
            {
                "title": "🎯 Ready to Start!",
                "description": "Let's begin your productivity journey",
                "features": ["Add your first task", "Explore the interface", "Try voice features", "Track your progress", "Achieve your goals"]
            }
        ]
        
        current_step = onboarding_steps[st.session_state.onboarding_step]
        
        # Progress bar
        progress = (st.session_state.onboarding_step + 1) / len(onboarding_steps)
        
        st.markdown(f"""
        <div class="onboarding-step">
            <h1>{current_step['title']}</h1>
            <p style="font-size: 1.2rem; margin: 1rem 0;">
                {current_step['description']}
            </p>
            
            <div class="onboarding-progress">
                <div class="onboarding-progress-bar" style="width: {progress * 100}%;"></div>
            </div>
            
            <div style="margin: 2rem 0;">
                <h3>✨ What makes MemoryMate special?</h3>
                <ul style="text-align: left; display: inline-block;">
        """, unsafe_allow_html=True)
        
        for feature in current_step['features']:
            st.markdown(f'<li>{feature}</li>', unsafe_allow_html=True)
        
        st.markdown("</ul></div>", unsafe_allow_html=True)
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.session_state.onboarding_step > 0:
                if st.button("⬅️ Previous", key="onboarding_prev"):
                    st.session_state.onboarding_step -= 1
                    st.rerun()
        
        with col2:
            if st.session_state.onboarding_step < len(onboarding_steps) - 1:
                if st.button("Next ➡️", key="onboarding_next"):
                    st.session_state.onboarding_step += 1
                    st.rerun()
            else:
                if st.button("🚀 Get Started", key="onboarding_start"):
                    st.session_state.onboarding_complete = True
                    st.rerun()
        
        with col3:
            if st.button("⏭️ Skip", key="onboarding_skip"):
                st.session_state.onboarding_complete = True
                st.rerun()


def render_kanban_board():
    """Render Kanban board view"""
    st.markdown("### 📋 Kanban Board View")
    
    all_tasks = st.session_state.assistant.task_manager.get_all_tasks()
    
    # Group tasks by status
    pending_tasks = [t for t in all_tasks if t.status == TaskStatus.PENDING]
    in_progress_tasks = [t for t in all_tasks if t.status == TaskStatus.IN_PROGRESS]
    completed_tasks = [t for t in all_tasks if t.status == TaskStatus.COMPLETED]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="kanban-column pending">
            <div class="kanban-column-header">⏳ Pending ({})</div>
        """.format(len(pending_tasks)), unsafe_allow_html=True)
        
        for task in pending_tasks:
            priority_class = "urgent" if task.priority == Priority.URGENT_IMPORTANT else "important" if task.priority == Priority.IMPORTANT_NOT_URGENT else "optional"
            st.markdown(f"""
            <div class="kanban-task {priority_class}">
                <h4>{task.title}</h4>
                {f'<p style="font-size: 0.9rem; color: var(--text-secondary);">{task.description}</p>' if task.description else ''}
                {f'<p style="font-size: 0.8rem; color: var(--text-secondary);">📅 {task.due_date}</p>' if task.due_date else ''}
                <div style="margin-top: 0.5rem;">
                    <span class="priority-badge priority-{task.priority.value.replace('_', '-')}">{task.priority.value.replace('_', ' ').title()}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Action buttons
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button(f"⏳ Start", key=f"kanban_start_{task.id}"):
                    task.status = TaskStatus.IN_PROGRESS
                    task.updated_at = datetime.now().isoformat()
                    st.session_state.assistant.task_manager.update_task(task)
                    st.rerun()
            with col_b:
                if st.button(f"✅ Complete", key=f"kanban_complete_{task.id}"):
                    task.status = TaskStatus.COMPLETED
                    task.updated_at = datetime.now().isoformat()
                    st.session_state.assistant.task_manager.update_task(task)
                    st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="kanban-column in-progress">
            <div class="kanban-column-header">🚀 In Progress ({})</div>
        """.format(len(in_progress_tasks)), unsafe_allow_html=True)
        
        for task in in_progress_tasks:
            priority_class = "urgent" if task.priority == Priority.URGENT_IMPORTANT else "important" if task.priority == Priority.IMPORTANT_NOT_URGENT else "optional"
            st.markdown(f"""
            <div class="kanban-task {priority_class}">
                <h4>{task.title}</h4>
                {f'<p style="font-size: 0.9rem; color: var(--text-secondary);">{task.description}</p>' if task.description else ''}
                {f'<p style="font-size: 0.8rem; color: var(--text-secondary);">📅 {task.due_date}</p>' if task.due_date else ''}
                <div style="margin-top: 0.5rem;">
                    <span class="priority-badge priority-{task.priority.value.replace('_', '-')}">{task.priority.value.replace('_', ' ').title()}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Action buttons
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button(f"⏸️ Pause", key=f"kanban_pause_{task.id}"):
                    task.status = TaskStatus.PENDING
                    task.updated_at = datetime.now().isoformat()
                    st.session_state.assistant.task_manager.update_task(task)
                    st.rerun()
            with col_b:
                if st.button(f"✅ Complete", key=f"kanban_complete_progress_{task.id}"):
                    task.status = TaskStatus.COMPLETED
                    task.updated_at = datetime.now().isoformat()
                    st.session_state.assistant.task_manager.update_task(task)
                    st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="kanban-column completed">
            <div class="kanban-column-header">✅ Completed ({})</div>
        """.format(len(completed_tasks)), unsafe_allow_html=True)
        
        for task in completed_tasks:
            priority_class = "urgent" if task.priority == Priority.URGENT_IMPORTANT else "important" if task.priority == Priority.IMPORTANT_NOT_URGENT else "optional"
            st.markdown(f"""
            <div class="kanban-task {priority_class}">
                <h4>{task.title}</h4>
                {f'<p style="font-size: 0.9rem; color: var(--text-secondary);">{task.description}</p>' if task.description else ''}
                <div style="margin-top: 0.5rem;">
                    <span style="color: var(--success-color); font-weight: 600;">✅ Completed</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)


def check_achievements():
    """Check and award achievements"""
    all_tasks = st.session_state.assistant.task_manager.get_all_tasks()
    completed_tasks = [t for t in all_tasks if t.status == TaskStatus.COMPLETED]
    
    new_achievements = []
    
    # First task achievement
    if len(all_tasks) >= 1 and "🚀 First Task" not in st.session_state.achievements:
        new_achievements.append("🚀 First Task")
        st.session_state.achievements.append("🚀 First Task")
    
    # Task completion achievements
    if len(completed_tasks) >= 5 and "🎯 Task Master" not in st.session_state.achievements:
        new_achievements.append("🎯 Task Master")
        st.session_state.achievements.append("🎯 Task Master")
    
    if len(completed_tasks) >= 10 and "🏆 Productivity Champion" not in st.session_state.achievements:
        new_achievements.append("🏆 Productivity Champion")
        st.session_state.achievements.append("🏆 Productivity Champion")
    
    # Streak achievements
    if st.session_state.streak_count >= 3 and "🔥 Streak Master" not in st.session_state.achievements:
        new_achievements.append("🔥 Streak Master")
        st.session_state.achievements.append("🔥 Streak Master")
    
    if st.session_state.streak_count >= 7 and "🔥 Week Warrior" not in st.session_state.achievements:
        new_achievements.append("🔥 Week Warrior")
        st.session_state.achievements.append("🔥 Week Warrior")
    
    # Score achievements
    if st.session_state.productivity_score >= 90 and "⭐ High Performer" not in st.session_state.achievements:
        new_achievements.append("⭐ High Performer")
        st.session_state.achievements.append("⭐ High Performer")
    
    return new_achievements


def render_achievements():
    """Render achievements and notifications"""
    new_achievements = check_achievements()
    
    if new_achievements:
        for achievement in new_achievements:
            st.markdown(f"""
            <div class="achievement-unlocked">
                <h2>🏆 Achievement Unlocked!</h2>
                <h3>{achievement}</h3>
                <p>Congratulations! You've earned a new badge.</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Show all achievements
    if st.session_state.achievements:
        st.markdown("### 🏆 Your Achievements")
        for achievement in st.session_state.achievements:
            st.markdown(f'<span class="badge">{achievement}</span>', unsafe_allow_html=True)


def render_gamification():
    """Render gamification elements"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="streak-card">
            <h2>🔥 Streak</h2>
            <h1 style="font-size: 3rem; margin: 0;">{st.session_state.streak_count}</h1>
            <p>days of productivity</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="productivity-score">
            <h2>📊 Score</h2>
            <h1 style="font-size: 3rem; margin: 0;">{st.session_state.productivity_score}</h1>
            <p>productivity points</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: var(--bg-secondary); border-radius: 20px; padding: 2rem; text-align: center;">
            <h2>🏆 Badges</h2>
            <div style="margin: 1rem 0;">
        """, unsafe_allow_html=True)
        
        for badge in st.session_state.badges:
            st.markdown(f'<span class="badge">{badge}</span>', unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)


def render_ai_coach():
    """Render AI coach recommendations"""
    st.markdown("""
    <div class="ai-coach-card">
        <h2>🤖 AI Coach Mode</h2>
        <p style="font-size: 1.1rem; margin: 1rem 0;">
            Your personal productivity coach is here to help!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get AI recommendations
    try:
        all_tasks = st.session_state.assistant.task_manager.get_all_tasks()
        urgent_tasks = [t for t in all_tasks if t.priority == Priority.URGENT_IMPORTANT and t.status != TaskStatus.COMPLETED]
        
        if urgent_tasks:
            st.info(f"🎯 **Priority Focus**: You have {len(urgent_tasks)} urgent tasks. Consider starting with: '{urgent_tasks[0].title}'")
        
        if not all_tasks:
            st.success("🎉 **Great start!** Add your first task to begin your productivity journey.")
        elif len([t for t in all_tasks if t.status == TaskStatus.COMPLETED]) > 0:
            st.success("🚀 **Keep it up!** You're making great progress. Consider adding more tasks to maintain momentum.")
        
    except Exception as e:
        st.info("🤖 **AI Coach**: Ready to help you stay productive and organized!")


def render_dashboard():
    """Render enhanced main dashboard"""
    st.markdown('<h1 class="main-header">🧠 MemoryMate</h1>', unsafe_allow_html=True)
    st.markdown("### Your AI Productivity Assistant • 100% Offline • 100% Private", help="All data stays on your device")
    
    # Theme toggle and view mode
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        if st.button(f"🌙 Dark Mode" if st.session_state.theme == "light" else "☀️ Light Mode"):
            st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
            st.rerun()
    
    with col2:
        if st.button("📋 List View" if st.session_state.view_mode == "kanban" else "📊 Kanban View"):
            st.session_state.view_mode = "kanban" if st.session_state.view_mode == "list" else "list"
            st.rerun()
    
    with col3:
        if st.button("🎯 Focus Mode"):
            st.session_state.page = "Focus Mode"
            st.rerun()
    
    with col4:
        if st.button("📊 Analytics"):
            st.session_state.page = "Analytics"
            st.rerun()
    
    # Gamification
    render_gamification()
    
    # AI Coach
    render_ai_coach()
    
    # Motivational Quote
    st.markdown(f"""
    <div class="motivational-quote">
        "{get_motivational_quote()}"
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats with enhanced styling
    all_tasks = st.session_state.assistant.task_manager.get_all_tasks()
    pending_tasks = [t for t in all_tasks if t.status == TaskStatus.PENDING]
    completed_tasks = [t for t in all_tasks if t.status == TaskStatus.COMPLETED]
    urgent_tasks = [t for t in all_tasks if t.priority == Priority.URGENT_IMPORTANT and t.status != TaskStatus.COMPLETED]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <h3>📋 Total Tasks</h3>
            <h1 style="color: var(--primary-color); margin: 0;">{len(all_tasks)}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <h3>⏳ Pending</h3>
            <h1 style="color: var(--warning-color); margin: 0;">{len(pending_tasks)}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-container">
            <h3>✅ Completed</h3>
            <h1 style="color: var(--success-color); margin: 0;">{len(completed_tasks)}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-container">
            <h3>🔴 Urgent</h3>
            <h1 style="color: var(--danger-color); margin: 0;">{len(urgent_tasks)}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick add task with enhanced form
    st.markdown("### 🚀 Quick Add Task")
    with st.form("quick_add_task", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            task_title = st.text_input("Task Title", placeholder="e.g., Finish project report")
            task_description = st.text_area("Description (optional)", placeholder="Add details about your task...")
        
        with col2:
            task_due_date = st.date_input("Due Date (optional)")
            task_priority = st.selectbox(
                "Priority",
                [Priority.URGENT_IMPORTANT, Priority.IMPORTANT_NOT_URGENT, Priority.OPTIONAL],
                format_func=lambda x: x.value.replace('_', ' ').title()
            )
            task_tags = st.text_input("Tags (comma-separated)", placeholder="work, urgent, project")
        
        if st.form_submit_button("✨ Add Task"):
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
                
                # Update gamification
                st.session_state.productivity_score = min(100, st.session_state.productivity_score + 5)
                
                st.success("🎉 Task added successfully! +5 productivity points")
                st.rerun()
    
    # Task lists with enhanced styling
    st.markdown("### 📋 Your Tasks")
    
    # View mode toggle
    if st.session_state.view_mode == "kanban":
        render_kanban_board()
    else:
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            priority_filter = st.selectbox(
                "Filter by Priority",
                ["All", "Urgent & Important", "Important", "Optional"]
            )
        with col2:
            status_filter = st.selectbox(
                "Filter by Status",
                ["All", "Pending", "In Progress", "Completed"]
            )
        with col3:
            search_query = st.text_input("🔍 Search tasks", placeholder="Type to search...")
        
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
        
        # Display tasks with enhanced cards
        if filtered_tasks:
            for i, task in enumerate(filtered_tasks):
                priority_emoji = "🔴" if task.priority == Priority.URGENT_IMPORTANT else "🟡" if task.priority == Priority.IMPORTANT_NOT_URGENT else "🟢"
                status_emoji = "✅" if task.status == TaskStatus.COMPLETED else "⏳" if task.status == TaskStatus.IN_PROGRESS else "📝"
                
                # Determine card class
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
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                            <h3 style="margin: 0;">{priority_emoji} {status_emoji} {task.title}</h3>
                            <div>
                                <span class="priority-badge priority-{task.priority.value.replace('_', '-')}">{task.priority.value.replace('_', ' ').title()}</span>
                                <span class="status-badge status-{task.status.value.replace('_', '-')}">{task.status.value.replace('_', ' ').title()}</span>
                            </div>
                        </div>
                        {f'<p style="margin: 0.5rem 0; color: var(--text-secondary);">{task.description}</p>' if task.description else ''}
                        {f'<p style="margin: 0.5rem 0; color: var(--text-secondary);"><strong>📅 Due:</strong> {task.due_date}</p>' if task.due_date else ''}
                        {f'<p style="margin: 0.5rem 0; color: var(--text-secondary);"><strong>🏷️ Tags:</strong> {", ".join(task.tags)}</p>' if task.tags else ''}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Action buttons
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        if st.button(f"✅ Complete", key=f"complete_{i}"):
                            task.status = TaskStatus.COMPLETED
                            task.updated_at = datetime.now().isoformat()
                            st.session_state.assistant.task_manager.update_task(task)
                            
                            # Update gamification
                            st.session_state.productivity_score = min(100, st.session_state.productivity_score + 10)
                            st.session_state.streak_count += 1
                            
                            st.success("🎉 Task completed! +10 productivity points, +1 streak!")
                            st.rerun()
                    
                    with col2:
                        if st.button(f"⏳ Start", key=f"start_{i}"):
                            task.status = TaskStatus.IN_PROGRESS
                            task.updated_at = datetime.now().isoformat()
                            st.session_state.assistant.task_manager.update_task(task)
                            st.success("🚀 Task started!")
                            st.rerun()
                    
                    with col3:
                        if st.button(f"✏️ Edit", key=f"edit_{i}"):
                            st.info("Edit functionality coming soon!")
                    
                    with col4:
                        if st.button(f"🗑️ Delete", key=f"delete_{i}"):
                            st.session_state.assistant.task_manager.delete_task(task.id)
                            st.success("🗑️ Task deleted")
                            st.rerun()
        else:
            st.info("📝 No tasks found matching your filters. Add some tasks to get started!")
    
    # Render achievements
    render_achievements()


def render_chat():
    """Render enhanced AI chat interface"""
    st.markdown('<h1 class="main-header">💬 AI Chat</h1>', unsafe_allow_html=True)
    st.markdown("### Chat with your AI productivity assistant • 100% Private", help="All conversations stay on your device")
    
    # Chat history with enhanced styling
    for i, message in enumerate(st.session_state.chat_history):
        if message["role"] == "user":
            st.markdown(f"""
            <div style="background: var(--primary-color); color: white; padding: 1rem; border-radius: 20px; margin: 0.5rem 0; text-align: right;">
                <strong>You:</strong> {message['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: var(--bg-secondary); color: var(--text-primary); padding: 1rem; border-radius: 20px; margin: 0.5rem 0; border: 1px solid var(--border-color);">
                <strong>MemoryMate:</strong> {message['content']}
            </div>
            """, unsafe_allow_html=True)
    
    # Enhanced voice input section
    st.markdown("### 🎤 Voice Input")
    
    # Voice recording simulation
    if 'voice_recording' not in st.session_state:
        st.session_state.voice_recording = False
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if not st.session_state.voice_recording:
            if st.button("🎤 Start Voice Recording", key="start_voice"):
                st.session_state.voice_recording = True
                st.rerun()
        else:
            st.markdown("""
            <div class="voice-recording">
                <h3>🎤 Recording...</h3>
                <div class="voice-waveform">
                    <div class="voice-bar"></div>
                    <div class="voice-bar"></div>
                    <div class="voice-bar"></div>
                    <div class="voice-bar"></div>
                    <div class="voice-bar"></div>
                </div>
                <p>Speak now! Whisper.cpp will transcribe your voice.</p>
            </div>
            """, unsafe_allow_html=True)
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("⏹️ Stop Recording", key="stop_voice"):
                    st.session_state.voice_recording = False
                    st.success("🎤 Voice recorded! Processing with Whisper.cpp...")
                    st.rerun()
            
            with col_b:
                if st.button("❌ Cancel", key="cancel_voice"):
                    st.session_state.voice_recording = False
                    st.rerun()
    
    # Voice input button (mockup for hackathon)
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <p style="color: var(--text-secondary); margin-bottom: 1rem;">
            <strong>Voice Input Features:</strong>
        </p>
        <ul style="text-align: left; display: inline-block; color: var(--text-secondary);">
            <li>🎤 Voice Activity Detection (VAD)</li>
            <li>🔊 Offline speech recognition with Whisper.cpp</li>
            <li>🧠 AI-powered task parsing</li>
            <li>🔒 100% private - no audio leaves your device</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Text input
    user_input = st.text_input(
        "Type your message:",
        placeholder="e.g., 'Remind me to call mom tomorrow' or 'What's on my plate today?'"
    )
    
    if st.button("🚀 Send", key="send_chat"):
        if user_input.strip():
            # Process with AI assistant
            response = st.session_state.assistant.process_input(user_input.strip())
            
            # Add to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            
            st.rerun()
    
    # Quick actions with enhanced styling
    st.markdown("### ⚡ Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 Show My Tasks", key="quick_tasks"):
            response = st.session_state.assistant.process_input("What's on my plate today?")
            st.session_state.chat_history.append({"role": "user", "content": "What's on my plate today?"})
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col2:
        if st.button("📅 Daily Summary", key="quick_summary"):
            response = st.session_state.assistant.get_daily_summary()
            st.session_state.chat_history.append({"role": "user", "content": "Show me my daily summary"})
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col3:
        if st.button("❓ Help", key="quick_help"):
            response = st.session_state.assistant.process_input("What can you do?")
            st.session_state.chat_history.append({"role": "user", "content": "What can you do?"})
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()
    
    # AI capabilities showcase
    st.markdown("### 🤖 AI Capabilities")
    st.markdown("""
    <div style="background: var(--bg-secondary); border-radius: 16px; padding: 2rem; margin: 1rem 0; border: 1px solid var(--border-color);">
        <h4>🧠 What MemoryMate can do:</h4>
        <ul style="margin: 1rem 0;">
            <li><strong>Natural Language Processing:</strong> Understands complex requests</li>
            <li><strong>Task Parsing:</strong> Converts voice/text to structured tasks</li>
            <li><strong>Priority Classification:</strong> Automatically determines urgency</li>
            <li><strong>Context Awareness:</strong> Remembers your preferences</li>
            <li><strong>Memory Recall:</strong> Finds relevant past information</li>
        </ul>
        <p style="color: var(--text-secondary); font-style: italic;">
            All processing happens locally using LLaMA.cpp - no internet required!
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_focus_mode():
    """Render enhanced focus mode"""
    st.markdown('<h1 class="main-header">🎯 Focus Mode</h1>', unsafe_allow_html=True)
    st.markdown("### Single-task focus for maximum productivity • 100% Offline")
    
    # Get current focus task
    all_tasks = st.session_state.assistant.task_manager.get_all_tasks()
    focus_tasks = [t for t in all_tasks if t.status == TaskStatus.IN_PROGRESS]
    
    if not focus_tasks:
        st.info("📋 No tasks are currently in progress.")
        
        # Show available tasks to start
        pending_tasks = [t for t in all_tasks if t.status == TaskStatus.PENDING]
        if pending_tasks:
            st.markdown("### 🚀 Available tasks to start:")
            for i, task in enumerate(pending_tasks[:5]):
                if st.button(f"🎯 Start: {task.title}", key=f"start_focus_{i}"):
                    task.status = TaskStatus.IN_PROGRESS
                    task.updated_at = datetime.now().isoformat()
                    st.session_state.assistant.task_manager.update_task(task)
                    st.rerun()
        else:
            st.info("📝 No pending tasks. Add some tasks first!")
        return
    
    # Focus on the first in-progress task
    focus_task = focus_tasks[0]
    
    # Task display with enhanced styling
    st.markdown(f"""
    <div class="task-card urgent-task">
        <h2>🎯 Current Focus: {focus_task.title}</h2>
        {f'<p><strong>Description:</strong> {focus_task.description}</p>' if focus_task.description else ''}
        {f'<p><strong>Due:</strong> {focus_task.due_date}</p>' if focus_task.due_date else ''}
        <p><strong>Priority:</strong> {focus_task.priority.value.replace('_', ' ').title()}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Pomodoro timer with enhanced UI
    st.markdown("### ⏰ Pomodoro Timer")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🍅 Start 25min", key="pomodoro_25"):
            st.session_state.pomodoro_start = time.time()
            st.session_state.pomodoro_duration = 25 * 60
            st.rerun()
    
    with col2:
        if st.button("☕ Short Break (5min)", key="pomodoro_5"):
            st.session_state.pomodoro_start = time.time()
            st.session_state.pomodoro_duration = 5 * 60
            st.rerun()
    
    with col3:
        if st.button("🛌 Long Break (15min)", key="pomodoro_15"):
            st.session_state.pomodoro_start = time.time()
            st.session_state.pomodoro_duration = 15 * 60
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
    
    # Task actions
    st.markdown("### 🎯 Task Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✅ Mark Complete", key="focus_complete"):
            focus_task.status = TaskStatus.COMPLETED
            focus_task.updated_at = datetime.now().isoformat()
            st.session_state.assistant.task_manager.update_task(focus_task)
            
            # Update gamification
            st.session_state.productivity_score = min(100, st.session_state.productivity_score + 15)
            st.session_state.streak_count += 1
            
            st.success("🎉 Task completed! +15 productivity points, +1 streak!")
            st.rerun()
    
    with col2:
        if st.button("⏸️ Snooze (1 hour)", key="focus_snooze"):
            st.info("Task snoozed for 1 hour")
    
    with col3:
        if st.button("🔄 Switch Task", key="focus_switch"):
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
    
    motivation = random.choice(motivation_messages)
    st.info(f"💡 {motivation}")


def render_analytics():
    """Render analytics and insights"""
    st.markdown('<h1 class="main-header">📊 Analytics</h1>', unsafe_allow_html=True)
    st.markdown("### Your productivity insights • 100% Private Data")
    
    try:
        all_tasks = st.session_state.assistant.task_manager.get_all_tasks()
        
        if all_tasks:
            # Task completion over time
            completed_tasks = [t for t in all_tasks if t.status == TaskStatus.COMPLETED]
            pending_tasks = [t for t in all_tasks if t.status == TaskStatus.PENDING]
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Priority distribution
                priority_counts = {}
                for task in all_tasks:
                    priority = task.priority.value.replace('_', ' ').title()
                    priority_counts[priority] = priority_counts.get(priority, 0) + 1
                
                if priority_counts:
                    fig = px.pie(
                        values=list(priority_counts.values()),
                        names=list(priority_counts.keys()),
                        title="Task Priority Distribution",
                        color_discrete_map={
                            "Urgent Important": "#ef4444",
                            "Important Not Urgent": "#f59e0b",
                            "Optional": "#10b981"
                        }
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Status distribution
                status_counts = {}
                for task in all_tasks:
                    status = task.status.value.replace('_', ' ').title()
                    status_counts[status] = status_counts.get(status, 0) + 1
                
                if status_counts:
                    fig = px.bar(
                        x=list(status_counts.keys()),
                        y=list(status_counts.values()),
                        title="Task Status Distribution",
                        color=list(status_counts.values()),
                        color_continuous_scale="viridis"
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            # Productivity trends
            st.markdown("### 📈 Productivity Trends")
            
            # Weekly completion rate
            if completed_tasks:
                st.success(f"🎯 **Weekly Completion Rate**: {len(completed_tasks)} tasks completed this week")
            
            # Urgent task management
            urgent_tasks = [t for t in all_tasks if t.priority == Priority.URGENT_IMPORTANT]
            if urgent_tasks:
                completed_urgent = [t for t in urgent_tasks if t.status == TaskStatus.COMPLETED]
                st.info(f"🚨 **Urgent Task Management**: {len(completed_urgent)}/{len(urgent_tasks)} urgent tasks completed")
            
            # Streak information
            st.info(f"🔥 **Current Streak**: {st.session_state.streak_count} days of productivity")
            st.info(f"📊 **Productivity Score**: {st.session_state.productivity_score}/100 points")
            
        else:
            st.info("📝 No tasks yet. Start adding tasks to see your analytics!")
            
    except Exception as e:
        st.error(f"Error loading analytics: {e}")


def main():
    """Main application"""
    initialize_session_state()
    
    # Onboarding
    render_enhanced_onboarding()
    
    # Sidebar navigation
    st.sidebar.markdown("## 🧠 MemoryMate")
    st.sidebar.markdown("Your AI Productivity Assistant")
    st.sidebar.markdown("🔒 **100% Offline • 100% Private**")
    
    # Navigation
    page = st.sidebar.selectbox(
        "Navigation",
        ["Dashboard", "AI Chat", "Focus Mode", "Analytics"],
        index=["Dashboard", "AI Chat", "Focus Mode", "Analytics"].index(st.session_state.page)
    )
    
    # Update current page
    if page != st.session_state.page:
        st.session_state.page = page
        st.rerun()
    
    # Sidebar quick actions
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚡ Quick Actions")
    
    if st.sidebar.button("📊 Daily Summary"):
        try:
            summary = st.session_state.assistant.get_daily_summary()
            st.sidebar.markdown("### 📊 Daily Summary")
            st.sidebar.markdown(summary)
        except Exception as e:
            st.sidebar.error("Error loading summary")
    
    # Privacy reminder
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### 🔒 Privacy First
    - All data stays on your device
    - No internet required
    - No data collection
    - 100% private
    """)
    
    # Main content
    if page == "Dashboard":
        render_dashboard()
    elif page == "AI Chat":
        render_chat()
    elif page == "Focus Mode":
        render_focus_mode()
    elif page == "Analytics":
        render_analytics()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "🧠 **MemoryMate** - Offline AI Productivity Assistant | "
        "Built with Whisper.cpp, LLaMA.cpp, and FAISS | "
        "🔒 100% Private • 🌐 100% Offline"
    )


if __name__ == "__main__":
    main()