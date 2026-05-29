from abc import ABC, abstractmethod
from typing import List, Dict, Any
from src.models.data_contract import StandardizedNewsRecord

class BaseNewsAdapter(ABC):

    def __init__(self, raw_data: Dict[str, Any]):
        self.raw_data = raw_data

    
    @abstractmethod
    def normalize(self) -> List[StandardizedNewsRecord]:
        pass