from dataclasses import dataclass, asdict
from typing import Optional


# Define schema 
@dataclass
class StandardizedNewsRecord:
    id: str
    source: str
    title: str
    url: str
    published_at: str
    content: Optional[str] = None
    author: Optional[str] = None

    def to_dict(self):
        return asdict(self)
    