from pathlib import Path
from src.db.news_loader import NewsLoader

if __name__ == "__main__":
    loader = NewsLoader()
    
    print("--- Initializing Database Schema ---")
    loader.init_database()
    
    print("\n--- Loading Data from Staging ---")
    
    # 1. Define project root directory (two levels up from this file)
    # Path(__file__).resolve()  -> .../newslake/src/test_load_db.py
    # .parent                   -> .../newslake/src
    # .parent.parent            -> .../newslake
    base_dir = Path(__file__).resolve().parent.parent
    
    # 2. Resolve the absolute path to the test_outputs folder
    staging_directory = base_dir / 'test_outputs'
    
    print(f"Targeting staging directory at: {staging_directory}")
    
    # 3. Ensure the directory exists before trying to load from it
    if not staging_directory.exists():
        print(f"Error: Staging directory not found at {staging_directory}")
    else:
        # Cast the Path object to string to ensure compatibility with os module inside NewsLoader
        loader.load_json_to_db(str(staging_directory))