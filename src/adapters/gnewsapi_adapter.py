from typing import List, Dict, Any
from src.models.data_contract import StandardizedNewsRecord
from src.adapters.base_adapter import BaseNewsAdapter

class GNewsApiAdapter(BaseNewsAdapter):
    def normalize(self):
        """
        Transform Gnews.io specific JSON structure into the standard format
        """
        standardized_list = []

        # Extract the articles from raw JSON
        articles = self.raw_data.get('articles', [])
        
        if not articles:
            print("Warning: No articles found in the NewsAPI raw data.")
            return standardized_list
        
        for item in articles:
            if not item.get('title') or not item.get('url'):
                continue

            raw_url = item.get('url', '')
            record_id = item.get('id', '')
            source_infor = item.get('source', {})
            source_name = source_infor.get('name', 'gnewsapi_io')

            record = StandardizedNewsRecord(
                id=record_id,
                source=source_name,
                title=item.get('title'),
                url=raw_url,
                published_at=item.get('publishedAt', 'unknown_date'),
                content=item.get('description'),
                author=None
            )

            standardized_list.append(record)
        return standardized_list
    
