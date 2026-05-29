from typing import List, Dict, Any
import hashlib
from src.models.data_contract import StandardizedNewsRecord
from src.adapters.base_adapter import BaseNewsAdapter

class NewsApiAdapter(BaseNewsAdapter):

    def normalize(self) -> List[StandardizedNewsRecord]:
        """
        Transform NewsAPI.org specific JSON structure into the standard format.
        """
        standardized_list = []

        # Extract the articles array from the raw JSON payload
        articles = self.raw_data.get('articles', [])


        if not articles:
            print("Warning: No articles found in the NewsAPI raw data.")
            return standardized_list
        
        for item in articles:
            # Defensive programming: skip items without mandatory fields
            if not item.get('title') or not item.get('url'):
                continue

            # NewsAPI doesn't always provide a unique ID, so we generate a safe one by hashing the URL
            raw_url = item.get('url', '')
            record_id = hashlib.md5(raw_url.encode('utf-8')).hexdigest()

            # Extract source name safely, default to 'newsapi' if missing
            source_info = item.get('source', {})
            source_name = source_info.get('name', 'newsapi_org')


            record = StandardizedNewsRecord(
                id=record_id,
                source=source_name,
                title=item.get('title'),
                url=raw_url,
                published_at=item.get('publishedAt', 'unknown_date'),
                content=item.get('description'),
                author=item.get('author')
            )
            standardized_list.append(record)

        return standardized_list

