import sqlite3

def get_db_connection():
    conn = sqlite3.connect("todos.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create table if not exists
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            due_date TEXT,
            tags TEXT
        )
    ''')
    conn.commit()
    conn.close()