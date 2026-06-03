import json
import os
from src.db.postgres_client import PostgresClient


class NewsLoader:
    def __init__(self):
        self.db_client = PostgresClient()

    def init_database(self):
        """Run the schema creation script."""
        self.db_client.create_tables()

    def load_records(self, records):
        """Insert a list of record objects into the database."""
        # Define the upsert query for inserting or ignoring duplicates based on URL
        upsert_query = """
            INSERT INTO data_pipeline.news_articles
                (
                    id,
                    source,
                    title,
                    url,
                    published_at,
                    content,
                    author
                )
            VALUES %s
            ON CONFLICT (url) DO NOTHING;
        """

        # Extract required fields from the records list into a list of tuples
        values = [
            (
                record.id,
                record.source,
                record.title,
                record.url,
                record.published_at,
                record.content,
                record.author
            )
            for record in records
        ]

        # Execute the bulk upsert operation in the database
        return self.db_client.bulk_upsert(
            upsert_query,
            values
        )

    def load_json_to_db(self, staging_dir: str):
        """
        Read all JSON files in the staging directory and load them into PostgreSQL.
        """
        if not os.path.exists(staging_dir):
            print(f"Staging directory not found: {staging_dir}")
            return

        # The UPSERT query: If the URL already exists, it ignores the new record to prevent duplicates
        upsert_query = """
            INSERT INTO data_pipeline.news_articles 
                (id, source, title, url, published_at, content, author)
            VALUES %s
            ON CONFLICT (url) DO NOTHING;
        """

        total_inserted = 0

        for filename in os.listdir(staging_dir):
            if not filename.endswith('.json'):
                continue

            filepath = os.path.join(staging_dir, filename)
            print(f"Processing file: {filename}")

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    articles = json.load(f)

                if not articles:
                    continue

                # Convert list of dictionaries to list of tuples for execute_values
                values = [
                    (
                        item.get('id', 'unknown'),
                        item.get('source', 'unknown'),
                        item.get('title', ''),
                        item.get('url', ''),
                        # Fallback to None if date is missing or invalid, let DB handle it
                        item.get('published_at') if item.get('published_at') != 'unknown_date' else None,
                        item.get('content', ''),
                        item.get('author')
                    )
                    for item in articles
                ]

                # Execute the bulk operation
                success = self.db_client.bulk_upsert(upsert_query, values)
                
                if success:
                    print(f"Successfully processed {len(articles)} potential records from {filename}.")
                    total_inserted += len(articles)
                    
                    # Optional: Rename or move the file to an 'archive' folder so it's not processed again
                    # archive_path = filepath + ".processed"
                    # os.rename(filepath, archive_path)
                    
            except Exception as e:
                print(f"Error processing file {filename}: {e}")

        print(f"Finished loading process. Processed a total of {total_inserted} records (including ignored duplicates).")