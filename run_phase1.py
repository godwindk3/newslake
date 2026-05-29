import json
import os
from dotenv import load_dotenv
from src.clients.base_client import APIClient
from src.adapters.factory import AdapterFactory


load_dotenv()

def load_configs(config_path: str) -> list:
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)
    

def test_pipeline():
    config_file = os.path.join(os.path.dirname(__file__), 'configs', 'api_sources.json')
    api_configs = load_configs(config_file)
    client = APIClient()

    for config in api_configs:
        if not config.get("is_active"):
            continue

        print(f"\n--- Processing API: {config['api_id']} ---")

        req_details = config["request_details"]
        params = req_details.get("params", {})
        headers = req_details.get("headers", {})

        env_key_name = config.get("auth_env_key")
        if env_key_name:
            api_key = os.getenv(env_key_name)
            if not api_key:
                print(f"Error: {env_key_name} not found in .env. Skipping.")
                continue
            auth_type = config.get("auth_type")
            if auth_type == "param":
                params[config.get("auth_param_name")] = api_key
            elif auth_type == "header":

                prefix = config.get("auth_header_prefix", "")

                formatted_key = f"{prefix} {api_key}".strip()

                headers[config.get("auth_header_name")] = formatted_key

        raw_json = client.fetch(url=req_details["base_url"], params=params, headers=headers)
        if not raw_json:
            continue

        try:
            adapter_type = config.get("adapter_type")
            adapter = AdapterFactory.get_adapter(adapter_type, raw_json)

            clean_records = adapter.normalize()


            output_filename = f"test_output_{config['api_id']}.json"
            dict_records = [record.to_dict() for record in clean_records]

            with open(output_filename, 'w', encoding='utf-8') as f:
                json.dump(dict_records, f, ensure_ascii=False, indent=4)

            print(f"Successfully saved {len(clean_records)} records to {output_filename}")
        
        except ValueError as e:
            print(f"Factory Error: {e}")
    

if __name__ == "__main__":
    test_pipeline()

