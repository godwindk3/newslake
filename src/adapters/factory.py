from typing import Dict, Any, Type
from src.adapters.base_adapter import BaseNewsAdapter
from src.adapters.thenewsapi_adapter import TheNewsApiAdapter
from src.adapters.newsapi_adapter import NewsApiAdapter
# import new adapters here in the future

class AdapterFactory:

    _adapter_map: Dict[str, Type[BaseNewsAdapter]] = {
        # "thenewsapi": TheNewsApiAdapter,

        "newsapi": NewsApiAdapter,
    }

    @classmethod
    def get_adapter(cls, adapter_type: str, raw_data: Dict[str, Any]) -> BaseNewsAdapter:
        
        adapter_class = cls._adapter_map.get(adapter_type)

        if not adapter_class:
            raise ValueError(f"Adapter type '{adapter_type}' is not registered in AdapterFactory.")
        
        return adapter_class(raw_data)