#!/usr/bin/env python3
"""
PostgreSQL Setup Script for RAG News Summarizer
This script helps you set up PostgreSQL database for the project.
"""

import os
import sys
from dotenv import load_dotenv

def check_postgres_installation():
    """Check if PostgreSQL is installed and accessible."""
    try:
        import psycopg2
        print("psycopg2 is installed")
        return True
    except ImportError:
        print("psycopg2 is not installed")
        return False

def check_environment_file():
    """Check if .env file exists and has required variables."""
    if not os.path.exists('.env'):
        print(".env file not found")
        return False
    
    load_dotenv()
    required_vars = ['POSTGRES_HOST', 'POSTGRES_DB', 'POSTGRES_USER', 'POSTGRES_PASSWORD']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    print("Environment variables configured")
    return True

def test_connection():
    """Test connection to PostgreSQL database."""
    try:
        from db.postgres_functions import get_connection
        conn = get_connection()
        conn.close()
        print("PostgreSQL connection successful")
        return True
    except Exception as e:
        print(f"PostgreSQL connection failed: {e}")
        return False

def create_database():
    """Create the database if it doesn't exist."""
    try:
        import psycopg2
        from dotenv import load_dotenv
        
        load_dotenv()
        
        # Connect to default postgres database
        conn = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST'),
            database='postgres',
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            port=os.getenv('POSTGRES_PORT')
        )
        
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (os.getenv('POSTGRES_DB'),))
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(f"CREATE DATABASE {os.getenv('POSTGRES_DB')}")
            print(f"Database '{os.getenv('POSTGRES_DB')}' created")
        else:
            print(f"Database '{os.getenv('POSTGRES_DB')}' already exists")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error creating database: {e}")
        return False

def main():
    """Main setup function."""
    print("PostgreSQL Setup for RAG News Summarizer")
    print("=" * 50)
    
    # Step 1: Check dependencies
    print("\n1. Checking dependencies...")
    if not check_postgres_installation():
        return False
    
    # Step 2: Check environment configuration
    print("\n2. Checking environment configuration...")
    if not check_environment_file():
        return False
    
    # Step 3: Create database
    print("\n3. Setting up database...")
    if not create_database():
        return False
    
    # Step 4: Test connection
    print("\n4. Testing connection...")
    if not test_connection():
        return False
    
    print("\nPostgreSQL setup completed successfully!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 