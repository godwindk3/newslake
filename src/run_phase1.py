import json
from pathlib import Path
from dotenv import load_dotenv
from src.clients.base_client import APIClient
from src.adapters.factory import AdapterFactory

load_dotenv()

def load_configs(config_path: Path) -> list:
    """
    Load API configurations from the JSON file.
    """
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found at: {config_path}")
        
    with config_path.open('r', encoding='utf-8') as f:
        return json.load(f)
    

def test_pipeline():
    # 1. Define project root directory (two levels up from this file)
    # Path(__file__).resolve()  -> .../newslake/src/run_phase1.py
    # .parent                   -> .../newslake/src
    # .parent.parent            -> .../newslake
    base_dir = Path(__file__).resolve().parent.parent
    
    # 2. Resolve paths for configs and test_outputs using the base_dir
    config_file = base_dir / 'configs' / 'api_sources.json'
    output_dir = base_dir / 'test_outputs'
    
    # Ensure the target directory exists at the root level
    output_dir.mkdir(parents=True, exist_ok=True)

    api_configs = load_configs(config_file)

    # Initialize a single client instance to reuse the connection pool
    client = APIClient()

    for config in api_configs:
        if not config.get("is_active"):
            print(f"Skipping inactive API: {config.get('api_id')}")
            continue

        print(f"\n--- Processing API: {config['api_id']} ---")

        try:
            # 3. EXTRACT: Pass the config to the client to handle auth and networking
            raw_json = client.fetch(config)
            if not raw_json:
                print(f"No data returned for {config['api_id']}. Moving to next API.")
                continue

            # 4. TRANSFORM: Pass the raw JSON to the Factory to instantiate the correct adapter
            adapter_type = config.get("adapter_type")
            adapter = AdapterFactory.get_adapter(adapter_type, raw_json)
            clean_records = adapter.normalize()

            # 5. LOAD: Save the standardized records to the test_outputs folder
            output_filename = f"{config['api_id']}_staging.json"
            output_filepath = output_dir / output_filename
            
            dict_records = [record.to_dict() for record in clean_records]

            # Pathlib objects have their own .open() method!
            with output_filepath.open('w', encoding='utf-8') as f:
                json.dump(dict_records, f, ensure_ascii=False, indent=4)
            
            print(f"Successfully saved {len(clean_records)} records to {output_filepath}")
        
        except Exception as e:
            print(f"Failed to process {config['api_id']}. Error: {e}")
                

if __name__ == "__main__":
    test_pipeline()