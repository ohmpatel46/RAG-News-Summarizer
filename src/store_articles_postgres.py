import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.postgres_functions import create_table, insert_article
from api.fetch_articles import fetch_articles

if __name__ == "__main__":

    # Create PostgreSQL table
    print("Setting up PostgreSQL table...")
    create_table()

    # Fetch Articles for the Topic "AI"
    article_topic="War"
    print("Fetching AI-related articles from November 2024...")
    articles = fetch_articles(query=article_topic, from_date="2025-06-16", to_date="2025-06-30")

    # Store Articles in the PostgreSQL Database
    if articles:
        print(f"Fetched {len(articles)} articles. Storing them in PostgreSQL...")
        for i, article in enumerate(articles, 1):
            try:
                insert_article(
                    title=article["title"],
                    author=article["author"],
                    description=article["description"],
                    content=article["content"],
                    published_at=article["publishedAt"],
                    url=article["url"],
                    source=article["source"]
                )
                
                if i % 10 == 0:
                    print(f"Stored {i}/{len(articles)} articles...")
                    
            except Exception as e:
                print(f"Error storing article {i}: {e}")
                continue
                
        print("All articles have been stored in PostgreSQL.")
    else:
        print("No articles fetched.") 