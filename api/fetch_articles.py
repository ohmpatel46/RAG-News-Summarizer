import requests
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")


def fetch_articles(query="AI", from_date="2024-11-01", to_date="2024-11-30", page_size=100):
    """
    Fetch articles from NewsAPI for the given query and date range.
    """
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "from": from_date,
        "to": to_date,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": page_size,
        "apiKey": NEWS_API_KEY
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])
        return [
            {
                "title": article.get("title"),
                "author": article.get("author"),
                "description": article.get("description"),
                "content": article.get("content"),
                "publishedAt": article.get("publishedAt"),
                "url": article.get("url"),
                "source": article["source"].get("name")
            }
            for article in articles
        ]
    else:
        print(f"Error: {response.status_code}, {response.json()}")
        return []
