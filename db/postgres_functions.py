import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'database': os.getenv('POSTGRES_DB', 'rag_news'),
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'password': os.getenv('POSTGRES_PASSWORD', ''),
    'port': int(os.getenv('POSTGRES_PORT', '5432'))
}

def get_connection():
    """Get a connection to PostgreSQL database."""
    return psycopg2.connect(**DB_CONFIG)

def create_table():
    """Create the articles table in PostgreSQL database if it doesn't exist."""
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id SERIAL PRIMARY KEY,
            title TEXT,
            author TEXT,
            description TEXT,
            content TEXT,
            published_at TIMESTAMP,
            url TEXT,
            source TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create index for better query performance
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_articles_published_at 
        ON articles(published_at)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_articles_source 
        ON articles(source)
    """)
    
    connection.commit()
    cursor.close()
    connection.close()
    print("PostgreSQL table 'articles' created successfully!")

def insert_article(title, author, description, content, published_at, url, source):
    """Insert a single article into the PostgreSQL database."""
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
        INSERT INTO articles (title, author, description, content, published_at, url, source)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (title, author, description, content, published_at, url, source))
    
    connection.commit()
    cursor.close()
    connection.close()

def get_articles(limit=10, offset=0):
    """Get articles from PostgreSQL database."""
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    
    cursor.execute("""
        SELECT * FROM articles 
        ORDER BY published_at DESC 
        LIMIT %s OFFSET %s
    """, (limit, offset))
    
    articles = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return articles

def search_articles(query, limit=10):
    """Search articles by title or content."""
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    
    cursor.execute("""
        SELECT * FROM articles 
        WHERE title ILIKE %s OR content ILIKE %s
        ORDER BY published_at DESC 
        LIMIT %s
    """, (f'%{query}%', f'%{query}%', limit))
    
    articles = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return articles

def get_article_count():
    """Get total number of articles in the database."""
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM articles")
    count = cursor.fetchone()[0]
    
    cursor.close()
    connection.close()
    
    return count 