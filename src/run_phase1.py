import json
import os
from dotenv import load_dotenv
from src.clients.base_client import APIClient
from src.adapters.factory import AdapterFactory


load_dotenv()

def load_configs(config_path: str) -> list:
    """
    Load API configurations from the JSON file.
    """
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)
    

def test_pipeline():
    config_file = os.path.join(os.path.dirname(__file__), 'configs', 'api_sources.json')
    api_configs = load_configs(config_file)

    # Initialize a single client instance to reuse the connection pool
    client = APIClient()

    for config in api_configs:
        if not config.get("is_active"):
            print(f"Skipping inactive API: {config.get('api_id')}")
            continue

        print(f"\n--- Processing API: {config['api_id']} ---")

        try:
            # 1. EXTRACT: Pass the config to the client to handle auth and networking
            raw_json = client.fetch(config)
            if not raw_json:
                print(f"No data returned for {config['api_id']}. Moving to next API.")
                continue

            # 2. TRANSFORM: Pass the raw JSON to the Factory to instantiate the correct adapter
            adapter_type = config.get("adapter_type")
            adapter = AdapterFactory.get_adapter(adapter_type, raw_json)
            clean_records = adapter.normalize()

            # 3. LOAD: Save the standardized records to a local JSON file (For Phase 1 testing)
            output_filename = f"test_output_{config['api_id']}.json"
            dict_records = [record.to_dict() for record in clean_records]

            with open(output_filename, 'w', encoding='utf-8') as f:
                json.dump(dict_records, f, ensure_ascii=False, indent=4)
            
            print(f"Successfully saved {len(clean_records)} records to {output_filename}")
        
        except Exception as e:
            print(f"Failed to process {config['api_id']}. Error: {e}")
                

    
if __name__ == "__main__":
    test_pipeline()

