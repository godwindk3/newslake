from typing import List, Dict, Any
from src.models.data_contract import StandardizedNewsRecord
from src.adapters.base_adapter import BaseNewsAdapter

class TheNewsApiAdapter(BaseNewsAdapter):
    
    def normalize(self) -> List[StandardizedNewsRecord]:
        
        standardized_list = []

        articles = self.raw_data.get('data', [])

        if not articles:
            print("Warning: No articles found in the raw data.")
            return standardized_list
        
        for item in articles:

            if not item.get('title') or not item.get('url'):
                continue

            record = StandardizedNewsRecord(
                id=item.get('uuid', 'unknown_id'),
                source=item.get('source', 'thenewsapi'),
                title=item.get('title'),
                url=item.get('url'),
                published_at=item.get('published_at', 'unknown_date'),
                content=item.get('description'),
                author=None
            )
            standardized_list.append(record)

        return standardized_list