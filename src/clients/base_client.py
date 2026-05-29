import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class APIClient:
    def __init__(self):
        # Configure retry strategy for resilient network calls
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )

        self.session = requests.Session()
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def _inject_auth(self, config: dict, params: dict, headers: dict) -> None:
        """
        Private method to parse config, retrieve API key from .env, 
        and inject it into the appropriate request location.
        """
        env_key_name = config.get("auth_env_key")
        if not env_key_name:
            # Skip if API does not require authentication
            return
        
        api_key = os.getenv(env_key_name)
        if not api_key:
            raise ValueError(f"CRITICAL: {env_key_name} not found in .env file!")
        
        auth_type = config.get("auth_type")

        if auth_type == "param":
            params[config.get("auth_param_name")] = api_key
        elif auth_type == "header":
            prefix = config.get("auth_header_prefix", "")

            headers[config.get("auth_header_name")] = f"{prefix} {api_key}".strip()
        
    def fetch(self, config: dict) -> dict:
        """
        Executes the GET request based on the provided configuration.
        """

        req_details = config.get("request_details", {})
        url = req_details.get("base_url")
        timeout = req_details.get("timeout", 10)

        # Use .copy() to avoid mutating the original configuration dictionary

        params = req_details.get("params", {}).copy()
        headers = req_details.get("headers", {}).copy()

        self._inject_auth(config, params, headers)

        print(f"Fetching data from: {url}")

        try:
            response = self.session.request(
                method=req_details.get("method", "GET"),
                url=url,
                params=params,
                headers=headers,
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Network error occurred: {e}")
            return {}








    # def fetch(self, url: str, params: dict = None, headers: dict = None) -> dict:
    #     """
    #     Executes the GET request based on the provided configuration.
    #     """
        
        

    #     print(f"Fetching data from: {url}")
    #     try:
    #         response = self.session.get(url, params=params, headers=headers, timeout=10)
    #         response.raise_for_status()
    #         return response.json()
    #     except requests.exceptions.RequestException as e:
    #         print(f"Network error occurred: {e}")
    #         return {}
