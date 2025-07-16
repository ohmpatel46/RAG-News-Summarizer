import os
from langchain.embeddings import HuggingFaceEmbeddings
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# PostgreSQL connection settings
DB_CONFIG = {
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'database': os.getenv('POSTGRES_DB', 'rag_news'),
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'password': os.getenv('POSTGRES_PASSWORD', ''),
    'port': int(os.getenv('POSTGRES_PORT', '5432'))
}

# Load the embedding model using LangChain
embeddings = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")

# Connect to PostgreSQL
def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def fetch_articles_without_embedding():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, content FROM articles WHERE embedding IS NULL")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def update_embeddings(updates):
    conn = get_connection()
    cur = conn.cursor()
    # Use execute_values for efficient batch update
    execute_values(
        cur,
        """
        UPDATE articles SET embedding = data.embedding
        FROM (VALUES %s) AS data(id, embedding)
        WHERE articles.id = data.id
        """,
        updates,
        template="(%s, %s)"
    )
    conn.commit()
    cur.close()
    conn.close()

def main():
    print("Fetching articles without embeddings...")
    articles = fetch_articles_without_embedding()
    print(f"Found {len(articles)} articles to embed.")
    
    updates = []
    contents = [content for _, content in articles]
    # Generate embeddings in batch for efficiency
    if contents:
        batch_embeddings = embeddings.embed_documents(contents)
        for (article_id, _), emb in zip(articles, batch_embeddings):
            updates.append((article_id, emb))
    
    if updates:
        print(f"Updating {len(updates)} articles with embeddings...")
        update_embeddings(updates)
        print("Embeddings updated successfully!")
    else:
        print("No articles to update.")

if __name__ == "__main__":
    main() 