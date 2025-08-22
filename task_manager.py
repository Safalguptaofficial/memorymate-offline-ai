import sqlite3
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class Priority(Enum):
    URGENT_IMPORTANT = "urgent_important"
    IMPORTANT_NOT_URGENT = "important_not_urgent"
    OPTIONAL = "optional"


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class Task:
    id: Optional[int]
    title: str
    description: str
    due_date: Optional[str]
    priority: Priority
    status: TaskStatus
    tags: List[str]
    created_at: str
    updated_at: str
    ai_notes: Optional[str] = None


class TaskManager:
    def __init__(self, db_path="memorymate.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()
    
    def _create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT,
            priority TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            tags TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            ai_notes TEXT
        )''')
        self.conn.commit()
    
    def add_task(self, task: Task) -> int:
        tags_json = json.dumps(task.tags)
        self.cursor.execute('''INSERT INTO tasks 
            (title, description, due_date, priority, status, tags, created_at, updated_at, ai_notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (task.title, task.description, task.due_date, task.priority.value,
             task.status.value, tags_json, task.created_at, task.updated_at, task.ai_notes))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def update_task(self, task: Task) -> bool:
        if not task.id:
            return False
        
        tags_json = json.dumps(task.tags)
        self.cursor.execute('''UPDATE tasks SET 
            title=?, description=?, due_date=?, priority=?, status=?, tags=?, updated_at=?, ai_notes=?
            WHERE id=?''',
            (task.title, task.description, task.due_date, task.priority.value,
             task.status.value, tags_json, task.updated_at, task.ai_notes, task.id))
        self.conn.commit()
        return True
    
    def get_task(self, task_id: int) -> Optional[Task]:
        self.cursor.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
        row = self.cursor.fetchone()
        if row:
            return self._row_to_task(row)
        return None
    
    def get_tasks_by_priority(self, priority: Priority) -> List[Task]:
        self.cursor.execute("SELECT * FROM tasks WHERE priority=? ORDER BY due_date ASC", (priority.value,))
        return [self._row_to_task(row) for row in self.cursor.fetchall()]
    
    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        self.cursor.execute("SELECT * FROM tasks WHERE status=? ORDER BY due_date ASC", (status.value,))
        return [self._row_to_task(row) for row in self.cursor.fetchall()]
    
    def get_all_tasks(self) -> List[Task]:
        self.cursor.execute("SELECT * FROM tasks ORDER BY priority DESC, due_date ASC")
        return [self._row_to_task(row) for row in self.cursor.fetchall()]
    
    def search_tasks(self, query: str) -> List[Task]:
        search_term = f"%{query}%"
        self.cursor.execute("""SELECT * FROM tasks 
            WHERE title LIKE ? OR description LIKE ? OR tags LIKE ?
            ORDER BY priority DESC, due_date ASC""", (search_term, search_term, search_term))
        return [self._row_to_task(row) for row in self.cursor.fetchall()]
    
    def delete_task(self, task_id: int) -> bool:
        self.cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        self.conn.commit()
        return True
    
    def _row_to_task(self, row) -> Task:
        tags = json.loads(row[6]) if row[6] else []
        return Task(
            id=row[0],
            title=row[1],
            description=row[2],
            due_date=row[3],
            priority=Priority(row[4]),
            status=TaskStatus(row[5]),
            tags=tags,
            created_at=row[7],
            updated_at=row[8],
            ai_notes=row[9]
        )
    
    def close(self):
        self.conn.close()


class AITaskParser:
    """AI-powered task parsing from natural language"""
    
    @staticmethod
    def parse_task_from_text(text: str) -> Task:
        """Parse natural language into a structured task"""
        now = datetime.now().isoformat()
        
        # Default values
        title = text.strip()
        description = ""
        due_date = None
        priority = Priority.OPTIONAL
        tags = []
        
        # Simple keyword-based parsing (can be enhanced with LLaMA)
        text_lower = text.lower()
        
        # Priority detection
        if any(word in text_lower for word in ['urgent', 'asap', 'emergency', 'critical']):
            priority = Priority.URGENT_IMPORTANT
        elif any(word in text_lower for word in ['important', 'priority', 'key']):
            priority = Priority.IMPORTANT_NOT_URGENT
        
        # Due date detection
        if 'tomorrow' in text_lower:
            due_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        elif 'next week' in text_lower:
            due_date = (datetime.now() + timedelta(weeks=1)).strftime('%Y-%m-%d')
        elif 'today' in text_lower:
            due_date = datetime.now().strftime('%Y-%m-%d')
        
        # Tag extraction
        if 'meeting' in text_lower:
            tags.append('meeting')
        if 'call' in text_lower:
            tags.append('call')
        if 'email' in text_lower:
            tags.append('email')
        if 'study' in text_lower:
            tags.append('study')
        if 'work' in text_lower:
            tags.append('work')
        
        return Task(
            id=None,
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            status=TaskStatus.PENDING,
            tags=tags,
            created_at=now,
            updated_at=now
        )
