from typing import List, Dict, Any
from src.models.data_contract import StandardizedNewsRecord
from src.adapters.base_adapter import BaseNewsAdapter

class SpaceflightNewsAdapter(BaseNewsAdapter):
    
    def normalize(self) -> List[StandardizedNewsRecord]:
        """
        Transform Spaceflight News API (v4) JSON structure into the standard format.
        """
        standardized_list = []
        
        # SNAPI v4 wraps the articles in a 'results' array
        articles = self.raw_data.get('results', [])
        
        if not articles:
            print("Warning: No articles found in the Spaceflight News raw response.")
            return standardized_list
            
        for item in articles:
            # Defensive check for mandatory fields
            if not item.get('title') or not item.get('url'):
                continue
            
            # Map the fields to our standard data contract
            record = StandardizedNewsRecord(
                id=str(item.get('id', 'unknown_id')), # Force string id just in case it returns int
                source=item.get('news_site', 'spaceflight_news'), # They provide a clean 'news_site' field
                title=item.get('title'),
                url=item.get('url'),
                published_at=item.get('published_at', 'unknown_date'),
                content=item.get('summary'), # SNAPI uses 'summary' for the article description
                author=None # SNAPI usually does not provide specific author names
            )
            standardized_list.append(record)
            
        return standardized_list