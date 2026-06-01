from typing import List, Dict, Any
from src.models.data_contract import StandardizedNewsRecord
from src.adapters.base_adapter import BaseNewsAdapter

class NytAdapter(BaseNewsAdapter):
    
    def normalize(self) -> List[StandardizedNewsRecord]:
        """
        Transform New York Times Top Stories JSON structure into the standard format.
        """
        standardized_list = []
        
        # NYT Top Stories API places the articles in the 'results' array
        articles = self.raw_data.get('results', [])
        
        if not articles:
            print("Warning: No articles found in the New York Times raw response.")
            return standardized_list
            
        for item in articles:
            # Defensive check: NYT sometimes returns empty promo items, ensure title and url exist
            if not item.get('title') or not item.get('url'):
                continue
                
            # Enhance source name with the specific section (e.g., 'New York Times - technology')
            section = item.get('section', 'general')
            source_name = f"New York Times - {section}"
            
            # Map the fields to our standard data contract
            record = StandardizedNewsRecord(
                id=item.get('uri') or item.get('url') or 'unknown_id',
                source=source_name,
                title=item.get('title'),
                url=item.get('url'),
                published_at=item.get('published_date', 'unknown_date'),
                content=item.get('abstract'),
                author=item.get('byline')
            )
            standardized_list.append(record)
            
        return standardized_list