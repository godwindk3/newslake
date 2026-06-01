import xml.etree.ElementTree as ET
from typing import List, Dict, Any
from src.models.data_contract import StandardizedNewsRecord
from src.adapters.base_adapter import BaseNewsAdapter

class RssAdapter(BaseNewsAdapter):
    
    def normalize(self) -> List[StandardizedNewsRecord]:
        """
        Parse raw XML/RSS string and convert it to standardized records.
        Works universally for any standard RSS 2.0 feed (BBC, CNN, Reuters, etc.).
        """
        standardized_list = []
        raw_xml = self.raw_data.get("raw_text")
        
        if not raw_xml:
            print("Warning: No XML data found for RSS adapter.")
            return standardized_list

        try:
            # Parse the raw XML string into an ElementTree object
            root = ET.fromstring(raw_xml)
            
            # Extract the overall feed title to use as the source name (e.g., "BBC News - Home")
            channel_title_elem = root.find(".//channel/title")
            feed_source_name = channel_title_elem.text if channel_title_elem is not None else "RSS Feed"
            
            # Find all <item> tags (these represent individual news articles)
            items = root.findall(".//item")
            
            for item in items:
                title_elem = item.find("title")
                link_elem = item.find("link")
                
                # Title and link are mandatory for a valid record
                if title_elem is None or link_elem is None or not title_elem.text or not link_elem.text:
                    continue
                    
                pub_date_elem = item.find("pubDate")
                desc_elem = item.find("description")
                
                # RSS feeds sometimes use standard <author> or namespaced <dc:creator>
                author_elem = item.find("author")
                
                # Map the extracted XML text to our standard data contract
                record = StandardizedNewsRecord(
                    id=link_elem.text, # RSS typically uses the URL as the unique identifier
                    source=feed_source_name, 
                    title=title_elem.text,
                    url=link_elem.text,
                    published_at=pub_date_elem.text if pub_date_elem is not None else "unknown_date",
                    content=desc_elem.text if desc_elem is not None else "",
                    author=author_elem.text if author_elem is not None else None
                )
                standardized_list.append(record)
                
        except ET.ParseError as e:
            print(f"Failed to parse XML from RSS feed: {e}")
            
        return standardized_list