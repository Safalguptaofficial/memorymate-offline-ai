# memory/memory_store.py
import sqlite3
import json
import os
from datetime import datetime
from typing import List, Optional
import threading

class MemoryStore:
    """Thread-safe memory store using SQLite with connection per operation"""
    
    def __init__(self, db_path: str = "memorymate.db"):
        self.db_path = db_path
        self._lock = threading.Lock()
        self._init_db()
    
    def _get_connection(self):
        """Get a fresh connection for each operation to avoid threading issues"""
        return sqlite3.connect(self.db_path)
    
    def _init_db(self):
        """Initialize the database with proper schema"""
        with self._lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                
                # Check if table exists
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='memory'")
                table_exists = cursor.fetchone() is not None
                
                if not table_exists:
                    # Create new table with full schema
                    cursor.execute("""
                        CREATE TABLE memory (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            text TEXT NOT NULL,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                            embedding BLOB
                        )
                    """)
                else:
                    # Check if embedding column exists
                    cursor.execute("PRAGMA table_info(memory)")
                    columns = [column[1] for column in cursor.fetchall()]
                    
                    if 'embedding' not in columns:
                        # Add embedding column to existing table
                        cursor.execute("ALTER TABLE memory ADD COLUMN embedding BLOB")
                
                conn.commit()
            finally:
                conn.close()
    
    def add_memory(self, text: str, embedding: Optional[bytes] = None) -> int:
        """Add a new memory entry"""
        with self._lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                
                # Check if embedding column exists
                cursor.execute("PRAGMA table_info(memory)")
                columns = [column[1] for column in cursor.fetchall()]
                
                if 'embedding' in columns:
                    cursor.execute(
                        "INSERT INTO memory (text, embedding) VALUES (?, ?)",
                        (text, embedding)
                    )
                else:
                    # Fallback for old schema
                    cursor.execute(
                        "INSERT INTO memory (text) VALUES (?)",
                        (text,)
                    )
                
                conn.commit()
                return cursor.lastrowid
            finally:
                conn.close()
    
    def get_memory(self, memory_id: int) -> Optional[dict]:
        """Get a specific memory by ID"""
        with self._lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                
                # Check if embedding column exists
                cursor.execute("PRAGMA table_info(memory)")
                columns = [column[1] for column in cursor.fetchall()]
                
                if 'embedding' in columns:
                    cursor.execute(
                        "SELECT id, text, timestamp, embedding FROM memory WHERE id = ?",
                        (memory_id,)
                    )
                else:
                    cursor.execute(
                        "SELECT id, text, timestamp FROM memory WHERE id = ?",
                        (memory_id,)
                    )
                
                row = cursor.fetchone()
                if row:
                    if 'embedding' in columns:
                        return {
                            "id": row[0],
                            "text": row[1],
                            "timestamp": row[2],
                            "embedding": row[3]
                        }
                    else:
                        return {
                            "id": row[0],
                            "text": row[1],
                            "timestamp": row[2],
                            "embedding": None
                        }
                return None
            finally:
                conn.close()
    
    def search_memory(self, query: str, limit: int = 10) -> List[dict]:
        """Search memory by text content"""
        with self._lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                
                # Check if timestamp column exists
                cursor.execute("PRAGMA table_info(memory)")
                columns = [column[1] for column in cursor.fetchall()]
                
                if 'timestamp' in columns:
                    cursor.execute(
                        "SELECT id, text, timestamp FROM memory WHERE text LIKE ? ORDER BY timestamp DESC LIMIT ?",
                        (f"%{query}%", limit)
                    )
                    rows = cursor.fetchall()
                    return [
                        {
                            "id": row[0],
                            "text": row[1],
                            "timestamp": row[2]
                        }
                        for row in rows
                    ]
                else:
                    # Fallback for old schema
                    cursor.execute(
                        "SELECT id, text FROM memory WHERE text LIKE ? LIMIT ?",
                        (f"%{query}%", limit)
                    )
                    rows = cursor.fetchall()
                    return [
                        {
                            "id": row[0],
                            "text": row[1],
                            "timestamp": None
                        }
                        for row in rows
                    ]
            finally:
                conn.close()
    
    def get_recent_memories(self, limit: int = 20) -> List[dict]:
        """Get recent memories"""
        with self._lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                
                # Check if timestamp column exists
                cursor.execute("PRAGMA table_info(memory)")
                columns = [column[1] for column in cursor.fetchall()]
                
                if 'timestamp' in columns:
                    cursor.execute(
                        "SELECT id, text, timestamp FROM memory ORDER BY timestamp DESC LIMIT ?",
                        (limit,)
                    )
                else:
                    # Fallback for old schema
                    cursor.execute(
                        "SELECT id, text FROM memory ORDER BY id DESC LIMIT ?",
                        (limit,)
                    )
                
                rows = cursor.fetchall()
                if 'timestamp' in columns:
                    return [
                        {
                            "id": row[0],
                            "text": row[1],
                            "timestamp": row[2]
                        }
                        for row in rows
                    ]
                else:
                    return [
                        {
                            "id": row[0],
                            "text": row[1],
                            "timestamp": None
                        }
                        for row in rows
                    ]
            finally:
                conn.close()
    
    def delete_memory(self, memory_id: int) -> bool:
        """Delete a memory by ID"""
        with self._lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM memory WHERE id = ?", (memory_id,))
                conn.commit()
                return cursor.rowcount > 0
            finally:
                conn.close()
    
    def clear_all_memories(self):
        """Clear all memories"""
        with self._lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM memory")
                conn.commit()
            finally:
                conn.close()
    
    def get_memory_count(self) -> int:
        """Get total number of memories"""
        with self._lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM memory")
                return cursor.fetchone()[0]
            finally:
                conn.close()
