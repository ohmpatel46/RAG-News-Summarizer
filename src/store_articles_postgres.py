import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.postgres_functions import create_table, insert_article
from api.fetch_articles import fetch_articles
from langchain.embeddings import HuggingFaceEmbeddings

if __name__ == "__main__":
    # Create PostgreSQL table
    print("Setting up PostgreSQL table...")
    create_table()

    # Load embedding model using LangChain
    embeddings = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")

    # Fetch Articles for the Topic "War"
    article_topic = "War"
    print("Fetching War-related articles from November 2024...")
    articles = fetch_articles(query=article_topic, from_date="2024-11-01", to_date="2024-11-30")

    # Store Articles in the PostgreSQL Database with Embeddings
    if articles:
        print(f"Fetched {len(articles)} articles. Storing them in PostgreSQL with embeddings...")
        contents = [article["content"] for article in articles]
        # Generate embeddings in batch for efficiency
        batch_embeddings = embeddings.embed_documents(contents)
        for i, (article, embedding) in enumerate(zip(articles, batch_embeddings), 1):
            try:
                insert_article(
                    title=article["title"],
                    author=article["author"],
                    description=article["description"],
                    content=article["content"],
                    published_at=article["publishedAt"],
                    url=article["url"],
                    source=article["source"],
                    embedding=embedding
                )
                if i % 10 == 0:
                    print(f"Stored {i}/{len(articles)} articles...")
            except Exception as e:
                print(f"Error storing article {i}: {e}")
                continue
        print("All articles have been stored in PostgreSQL with embeddings.")
    else:
        print("No articles fetched.") 