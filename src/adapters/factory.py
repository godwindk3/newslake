from typing import Dict, Any, Type
from src.adapters.base_adapter import BaseNewsAdapter
from src.adapters.thenewsapi_adapter import TheNewsApiAdapter
from src.adapters.newsapi_adapter import NewsApiAdapter
from src.adapters.gnewsapi_adapter import GNewsApiAdapter
from src.adapters.newsdataapi_adapter import NewsDataApiAdapter
from src.adapters.currentnewsapi_adapter import CurrentsApiAdapter
from src.adapters.freenewsapi_adapter import FreeNewsApiAdapter
from src.adapters.theguardianapi_adapter import GuardianAdapter
from src.adapters.nytimes_adapter import NytAdapter
from src.adapters.eventregistry_adapter import EventRegistryAdapter
from src.adapters.spaceflightnews_adapter import SpaceflightNewsAdapter
from src.adapters.rss_adapter import RssAdapter
# import new adapters here in the future

class AdapterFactory:

    _adapter_map: Dict[str, Type[BaseNewsAdapter]] = {
        # "thenewsapi": TheNewsApiAdapter,
        # "newsapi": NewsApiAdapter,
        # "gnewsapi": GNewsApiAdapter,
        # "newsdataapi": NewsDataApiAdapter,
        # "currentsapi": CurrentsApiAdapter,
        # "freenewsapi": FreeNewsApiAdapter,
        # "guardian": GuardianAdapter,
        # "nytimes": NytAdapter,
        # "eventregistry": EventRegistryAdapter,
        # "spaceflightnews": SpaceflightNewsAdapter,
        "rss": RssAdapter,
        
    }

    @classmethod
    def get_adapter(cls, adapter_type: str, raw_data: Dict[str, Any]) -> BaseNewsAdapter:
        
        adapter_class = cls._adapter_map.get(adapter_type)

        if not adapter_class:
            raise ValueError(f"Adapter type '{adapter_type}' is not registered in AdapterFactory.")
        
        return adapter_class(raw_data)