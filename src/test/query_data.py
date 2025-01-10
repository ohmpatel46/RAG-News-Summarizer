import sqlite3

def query_articles():
    connection = sqlite3.connect('news.db')  # Ensure the correct path to your database
    cursor = connection.cursor()
    
    # Fetch all rows from the articles table
    cursor.execute("SELECT * FROM articles WHERE id=500 OR id=600 OR id=501 OR id=601")
    rows = cursor.fetchall()

    # Print the results
    for row in rows:
        print(f"ID: {row[0]}")
        print(f"Title: {row[1]}")
        print(f"Author: {row[2]}")
        print(f"Description: {row[3]}")
        print(f"Content: {row[4]}")
        print(f"Published At: {row[5]}")
        print(f"URL: {row[6]}")
        print(f"Source: {row[7]}")
        print("-" * 80)
    print(rows)
    connection.close()

if __name__ == "__main__":
    query_articles()
