import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.db_functions import create_table

if __name__ == "__main__":
    try:
        print("Creating the 'articles' table in the SQLite database...")
        create_table()
        print("Table 'articles' created successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
