# modules/utils.py

import sqlite3
import numpy as np
from config import DATABASE_PATH

def init_database():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            mobile TEXT NOT NULL,
            face_encoding BLOB NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            entry_time TIMESTAMP NOT NULL,
            access_key TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

def add_user(name, mobile, face_encoding):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    face_encoding_blob = face_encoding.tobytes()
    cursor.execute('''
        INSERT INTO users (name, mobile, face_encoding)
        VALUES (?, ?, ?)
    ''', (name, mobile, face_encoding_blob))
    conn.commit()
    conn.close()

def add_user_entry_log(name, access_key):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE name = ?', (name,))
    user_id = cursor.fetchone()[0]
    cursor.execute('''
        INSERT INTO entries (user_id, entry_time, access_key)
        VALUES (?, datetime('now'), ?)
    ''', (user_id, access_key))
    conn.commit()
    conn.close()        

def get_known_faces():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT name, face_encoding FROM users')
    rows = cursor.fetchall()
    conn.close()
    names = []
    encodings = []
    for row in rows:
        names.append(row[0])
        encodings.append(np.frombuffer(row[1], dtype=np.float64))
    return names, encodings


def generate_random_access_key():
    from random import randint
    key = [str(randint(1, 9)) for _ in range(3)]
    return ' '.join(key)
