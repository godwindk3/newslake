from typing import List, Dict, Any
from src.models.data_contract import StandardizedNewsRecord
from src.adapters.base_adapter import BaseNewsAdapter

class FreeNewsApiAdapter(BaseNewsAdapter):
    
    def normalize(self) -> List[StandardizedNewsRecord]:
        """
        Transform FreeNewsAPI.io specific JSON structure into the standard format.
        Implemented with advanced defensive checks to handle dynamic field names.
        """
        standardized_list = []
        
        # Attempt to find the main array, fallback to 'data' if 'articles' is missing
        articles = self.raw_data.get('articles') or self.raw_data.get('data') or []
        
        if not articles:
            print("Warning: No articles found in the FreeNewsAPI raw response.")
            return standardized_list
            
        for item in articles:
            # Smart URL extraction: Handle both 'url' and 'link' variations
            article_url = item.get('url') or item.get('link')
            
            # Mandatory fields check
            if not item.get('title') or not article_url:
                continue
                
            # Safely extract source information (handle both Dict and String types)
            source_info = item.get('source')
            if isinstance(source_info, dict):
                source_name = source_info.get('name', 'freenewsapi_io')
            elif isinstance(source_info, str):
                source_name = source_info
            else:
                source_name = 'freenewsapi_io'
                
            # Smart Date extraction: Handle various common datetime keys
            pub_date = item.get('publishedAt') or item.get('published_date') or item.get('date') or 'unknown_date'
            
            # Map the fields to our standard data contract
            record = StandardizedNewsRecord(
                id=item.get('id') or item.get('_id') or 'unknown_id',
                source=source_name,
                title=item.get('title'),
                url=article_url,
                published_at=pub_date,
                content=item.get('description') or item.get('content'),
                author=item.get('author') or item.get('creator')
            )
            standardized_list.append(record)
            
        return standardized_list