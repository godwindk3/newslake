import os
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

class PostgresClient:
    def __init__(self):
        """Initialize connection parameters from environment variables."""
        load_dotenv()
        self.db_url = os.getenv("DATABASE_URL")
        if not self.db_url:
            raise ValueError("DATABASE_URL is not set in the .env file")
        
        self.conn = None

    def connect(self):
        """Establish a connection to the PostgreSQL database."""
        try:
            self.conn = psycopg2.connect(self.db_url)
            self.conn.autocommit = False
            return self.conn
        except Exception as e:
            print(f"Failed to connect to database: {e}")
            raise

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()

    def create_tables(self):
        """Create the necessary schemas and tables if they do not exist."""
        schema_query = """
        CREATE SCHEMA IF NOT EXISTS data_pipeline;
        
        CREATE TABLE IF NOT EXISTS data_pipeline.news_articles (
            id VARCHAR(255) NOT NULL,
            source VARCHAR(100) NOT NULL,
            title TEXT NOT NULL,
            url TEXT PRIMARY KEY,
            published_at TIMESTAMPTZ,
            content TEXT,
            author TEXT,
            inserted_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_news_published_at ON data_pipeline.news_articles (published_at DESC);
        CREATE INDEX IF NOT EXISTS idx_news_source ON data_pipeline.news_articles (source);
        """
        try:
            with self.connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(schema_query)
                conn.commit()
                print("Database schema and tables verified/created successfully.")
        except Exception as e:
            print(f"Error creating tables: {e}")
            if self.conn:
                self.conn.rollback()

    def bulk_upsert(self, query: str, values: list):
        """
        Execute a bulk insert/upsert operation using execute_values for high performance.
        """
        try:
            with self.connect() as conn:
                with conn.cursor() as cur:
                    # execute_values is highly optimized for inserting multiple rows at once
                    execute_values(cur, query, values)
                conn.commit()
                return True
        except Exception as e:
            print(f"Bulk upsert failed: {e}")
            if self.conn:
                self.conn.rollback()
            return False