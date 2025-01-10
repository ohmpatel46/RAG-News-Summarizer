import requests
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_ai_articles_november2024():
    # Define endpoint and parameters
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "AI",                       # Search for AI
        "from": "2024-11-01",            # Start date
        "to": "2024-11-30",              # End date
        "language": "en",                # Language filter
        "sortBy": "publishedAt",         # Sort by date
        "pageSize": 10,                 # Max results per request
        "apiKey": NEWS_API_KEY           # Your API key
    }
    
    # Make the API request
    response = requests.get(url, params=params)
    
    # Check for successful response
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
                "source": article["source"].get("name")  # Source name
            }
            for article in articles
        ]
    else:
        print(f"Error: {response.status_code}, {response.json()}")
        return []

# Fetch AI articles
if __name__ == "__main__":
    articles = fetch_ai_articles_november2024()
    for article in articles:
        print(f"Title: {article['title']}")
        print(f"Author: {article['author']}")
        print(f"Description: {article['description']}")
        print(f"Published At: {article['publishedAt']}")
        print(f"Source: {article['source']}")
        print(f"URL: {article['url']}")
        print("-" * 80)
