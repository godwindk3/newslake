from typing import List, Dict, Any
from src.models.data_contract import StandardizedNewsRecord
from src.adapters.base_adapter import BaseNewsAdapter

class CurrentsApiAdapter(BaseNewsAdapter):
    
    def normalize(self) -> List[StandardizedNewsRecord]:
        """
        Transform Currents API specific JSON structure into the standard format.
        """
        standardized_list = []
        
        articles = self.raw_data.get('news', [])
        
        if not articles:
            print("Warning: No articles found in the Currents API raw response.")
            return standardized_list
            
        for item in articles:
            # Defensive check using the correct keys for Currents API
            if not item.get('title') or not item.get('url'):
                continue
                
            
            author_info = item.get('author')
            
            
            categories = item.get('category')
            if isinstance(categories, list) and len(categories) > 0:
                source_name = categories[0]
            elif isinstance(categories, str):
                source_name = categories
            else:
                source_name = 'currents_api'
            
            
            record = StandardizedNewsRecord(
                id=item.get('id', 'unknown_id'),
                source=source_name,
                title=item.get('title'),
                url=item.get('url'),
                published_at=item.get('published', 'unknown_date'),
                content=item.get('description'),
                author=author_info
            )
            standardized_list.append(record)
            
        return standardized_list