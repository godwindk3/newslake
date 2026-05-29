from typing import List, Dict, Any
from src.models.data_contract import StandardizedNewsRecord
from src.adapters.base_adapter import BaseNewsAdapter

class TheNewsApiAdapter(BaseNewsAdapter):
    
    def normalize(self) -> List[StandardizedNewsRecord]:
        """
        Transform TheNewsAPI specific JSON structure into our standard format.
        """
        
        standardized_list = []

        # TheNewsAPI wraps its list of articles inside a 'data' array
        articles = self.raw_data.get('data', [])

        if not articles:
            print("Warning: No articles found in the raw data.")
            return standardized_list
        
        for item in articles:
            # Defensive check: skip if essential fields are missing
            if not item.get('title') or not item.get('url'):
                continue

            # Map API fields to our StandardizedNewsRecord
            record = StandardizedNewsRecord(
                id=item.get('uuid', 'unknown_id'),
                source=item.get('source', 'thenewsapi'),
                title=item.get('title'),
                url=item.get('url'),
                published_at=item.get('published_at', 'unknown_date'),
                content=item.get('description'),
                author=None # TheNewsAPI free tier doesn't always provide author
            )
            standardized_list.append(record)

        return standardized_list