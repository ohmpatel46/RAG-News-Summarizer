import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.db_functions import create_table, insert_article
from api.fetch_articles import fetch_articles

if __name__ == "__main__":

    # Step 2: Fetch Articles for the Topic "AI"
    article_topic="War"
    print("Fetching AI-related articles from November 2024...")
    articles = fetch_articles(query=article_topic, from_date="2024-11-01", to_date="2024-11-30")

    # Step 3: Store Articles in the Database
    if articles:
        print(f"Fetched {len(articles)} articles. Storing them in the database...")
        for article in articles:
            insert_article(
                title=article["title"],
                author=article["author"],
                description=article["description"],
                content=article["content"],
                published_at=article["publishedAt"],
                url=article["url"],
                source=article["source"]
            )
        print("All articles have been stored.")
    else:
        print("No articles fetched.")
