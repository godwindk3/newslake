import json
from pathlib import Path

from src.clients.base_client import APIClient
from src.adapters.factory import AdapterFactory
from src.db.news_loader import NewsLoader


class NewsPipeline:

    def __init__(self):
        self.client = APIClient()
        self.loader = NewsLoader()

    def load_configs(self):

        root = Path(__file__).resolve().parents[2]

        config_file = root / "configs" / "api_sources.json"

        with open(config_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def run(self):

        self.loader.init_database()

        configs = self.load_configs()

        for config in configs:

            if not config.get("is_active"):
                continue

            print(f"Processing {config['api_id']}")

            try:

                raw_json = self.client.fetch(config)

                if not raw_json:
                    continue

                adapter = AdapterFactory.get_adapter(
                    config["adapter_type"],
                    raw_json
                )

                records = adapter.normalize()

                self.loader.load_records(records)

                print(
                    f"{config['api_id']} -> {len(records)} records"
                )

            except Exception as e:

                print(
                    f"{config['api_id']} failed: {e}"
                )