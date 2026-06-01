from typing import List, Dict, Any
from src.models.data_contract import StandardizedNewsRecord
from src.adapters.base_adapter import BaseNewsAdapter

class EventRegistryAdapter(BaseNewsAdapter):
    
    def normalize(self) -> List[StandardizedNewsRecord]:
        """
        Transform Event Registry API specific JSON structure into the standard format.
        """
        standardized_list = []
        
        # Event Registry nests the results inside an 'articles' object
        articles_obj = self.raw_data.get('articles', {})
        results = articles_obj.get('results', [])
        
        if not results:
            print("Warning: No articles found in the Event Registry raw response.")
            return standardized_list
            
        for item in results:
            # Defensive check for mandatory fields
            if not item.get('title') or not item.get('url'):
                continue
                
            # Safely extract source name (Event Registry wraps it in a source object)
            source_info = item.get('source', {})
            source_name = source_info.get('title', 'event_registry')
            
            # Safely extract author(s) - it's usually a list of dictionaries
            authors_list = item.get('authors', [])
            author_names = [author.get('name') for author in authors_list if isinstance(author, dict) and author.get('name')]
            # Join multiple authors with a comma, or set to None if empty
            author_string = ", ".join(author_names) if author_names else None
            
            # Extract publish date (prefer dateTime, fallback to date)
            pub_date = item.get('dateTime') or item.get('date') or 'unknown_date'
            
            # Map the fields to our standard data contract
            record = StandardizedNewsRecord(
                id=item.get('uri', 'unknown_id'),
                source=source_name,
                title=item.get('title'),
                url=item.get('url'),
                published_at=pub_date,
                content=item.get('body'),
                author=author_string
            )
            standardized_list.append(record)
            
        return standardized_list