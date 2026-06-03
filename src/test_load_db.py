from src.db.news_loader import NewsLoader

if __name__ == "__main__":
    loader = NewsLoader()
    
    print("--- Initializing Database Schema ---")
    loader.init_database()
    
    print("\n--- Loading Data from Staging ---")
    staging_directory = "test_output" 
    loader.load_json_to_db(staging_directory)