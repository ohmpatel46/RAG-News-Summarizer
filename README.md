# RAG-News-Summarizer

A Retrieval-Augmented Generation (RAG)-based application designed to provide concise and context-rich summaries of news articles. The system retrieves relevant background information and historical context to enhance the quality of its summaries, making it easier for users to stay informed.

## Project Overview
- **News articles** are fetched from NewsAPI and stored in a **PostgreSQL** database.
- The database currently contains articles related to AI, Bitcoin, Movies, Music, Election, and War from November 2024.
- The project is now fully migrated to PostgreSQL (no SQLite dependencies remain).

## Project Structure
```
.
├── api/
│   └── fetch_articles.py           # Fetches news articles from NewsAPI
├── db/
│   └── postgres_functions.py       # PostgreSQL database logic (create, insert, query, search)
├── src/
│   ├── store_articles_postgres.py  # Fetches and stores articles in PostgreSQL
│   └── scraper.py                  # Fetches and prints articles (for testing/debugging)
├── data/                           # (Empty, for future data assets)
├── environment.yml                 # Conda environment dependencies
├── README.md                       # Project documentation
├── .gitignore                      # Git ignore rules
```

## Setup Instructions
1. **Install PostgreSQL** and ensure it is running.
2. **Create a Conda environment** from `environment.yml`:
   ```bash
   conda env create -f environment.yml
   conda activate RAG_news_summarizer
   ```
3. **Create a `.env` file** (copy from `env_example.txt` if available) and fill in your PostgreSQL credentials and NewsAPI key.
4. **Run the setup script** (if you kept it) to initialize the database, or manually run the table creation logic from `postgres_functions.py`.
5. **Fetch and store articles**:
   ```bash
   python src/store_articles_postgres.py
   ```

## Next Steps for Development
- **Implement RAG Pipeline:**
  - Add vector embedding and similarity search (e.g., using pgvector or a vector DB)
  - Integrate a language model (LLM) for generating summaries
  - Build the retrieval-augmented generation workflow
- **Develop a User Interface:**
  - CLI, web app, or API for users to query and receive summaries
- **Enhance Data Pipeline:**
  - Add more topics, sources, or time ranges
  - Automate regular article fetching
- **Testing & Deployment:**
  - Add tests for database and pipeline logic
  - Prepare for deployment (Docker, cloud, etc.)

## Contact
For questions or contributions, please open an issue or pull request.