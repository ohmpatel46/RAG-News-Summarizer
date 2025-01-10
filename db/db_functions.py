import sqlite3

DB_FILE = "news.db"

def create_table():
    """Create the articles table in SQLite database if it doesn't exist."""
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            description TEXT,
            content TEXT,
            published_at TEXT,
            url TEXT,
            source TEXT
        )
    """)
    connection.commit()
    connection.close()

def insert_article(title, author, description, content, published_at, url, source):
    """Insert a single article into the database."""
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO articles (title, author, description, content, published_at, url, source)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (title, author, description, content, published_at, url, source))
    connection.commit()
    connection.close()
