# memory/memory_store.py
import os
import sqlite3
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class MemoryStore:
    def __init__(self, db_path="memorymate.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self._create_tables()
        self._load_index()

    def _create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS memory (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                text TEXT NOT NULL
                              )''')
        self.conn.commit()

    def _load_index(self):
        self.index = faiss.IndexFlatL2(384)  # dimension of MiniLM-L6-v2
        self.texts = []
        self.ids = []

        self.cursor.execute("SELECT id, text FROM memory")
        rows = self.cursor.fetchall()
        for _id, text in rows:
            embedding = self._embed(text)
            self.index.add(np.array([embedding]).astype('float32'))
            self.ids.append(_id)
            self.texts.append(text)

    def _embed(self, text):
        return self.model.encode(text)

    def add_memory(self, text):
        self.cursor.execute("INSERT INTO memory (text) VALUES (?)", (text,))
        self.conn.commit()
        embedding = self._embed(text)
        self.index.add(np.array([embedding]).astype('float32'))
        self.ids.append(self.cursor.lastrowid)
        self.texts.append(text)

    def search_memory(self, query, k=3):
        if self.index.ntotal == 0:
            return []
        embedding = self._embed(query)
        D, I = self.index.search(np.array([embedding]).astype('float32'), k)
        return [self.texts[i] for i in I[0] if i != -1]
