from typing import List, Dict, Any
from src.models.data_contract import StandardizedNewsRecord
from src.adapters.base_adapter import BaseNewsAdapter

class GuardianAdapter(BaseNewsAdapter):
    
    def normalize(self) -> List[StandardizedNewsRecord]:
        """
        Transform The Guardian API specific JSON structure into the standard format.
        """
        standardized_list = []
        
        # The Guardian API nests the articles array inside a 'response' object under 'results'
        response_data = self.raw_data.get('response', {})
        articles = response_data.get('results', [])
        
        if not articles:
            print("Warning: No articles found in The Guardian API raw response.")
            return standardized_list
            
        for item in articles:
            # Mandatory fields check using The Guardian's specific keys
            if not item.get('webTitle') or not item.get('webUrl'):
                continue
                
            # Optional fields are explicitly requested via 'show-fields' parameter
            fields = item.get('fields', {})
            
            # Create a robust source name combining the publication and the specific section
            section = item.get('sectionName', 'General')
            source_name = f"The Guardian - {section}"
            
            # Map the fields to our standard data contract
            record = StandardizedNewsRecord(
                id=item.get('id', 'unknown_id'),
                source=source_name,
                title=item.get('webTitle'),
                url=item.get('webUrl'),
                published_at=item.get('webPublicationDate', 'unknown_date'),
                content=fields.get('trailText'),
                author=fields.get('byline')
            )
            standardized_list.append(record)
            
        return standardized_list