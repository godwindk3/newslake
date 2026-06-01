from typing import List, Dict, Any
from src.models.data_contract import StandardizedNewsRecord
from src.adapters.base_adapter import BaseNewsAdapter

class NewsDataApiAdapter(BaseNewsAdapter):
    def normalize(self) -> List[StandardizedNewsRecord]:
        """
        Transform Newsdata specific JSON structure into my standard
        """
        standardized_list = []

        articles = self.raw_data.get('results', [])

        if not articles:
            print("Warning: No articles found in the raw data.")
            return standardized_list
        
        for item in articles:
            if not item.get('title') or not item.get('link'):
                continue

            raw_url = item.get('link', '')
            record_id = item.get('article_id', '')
            source_name = item.get('source_name', 'newsdataapi_io')
            title = item.get('title')
            published_at = item.get('pubDate', 'unknown_date')
            content = item.get('description')
            author = item.get('creator', None)

            record = StandardizedNewsRecord(
                id=record_id,
                source=source_name,
                title=title,
                url=raw_url,
                published_at=published_at,
                content=content,
                author=author
            )

            standardized_list.append(record)
        
        return standardized_list
