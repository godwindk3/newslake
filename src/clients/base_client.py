import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class APIClient:
    def __init__(self):
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )

        self.session = requests.Session()
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def fetch(self, url: str, params: dict = None, headers: dict = None) -> dict:
        
        print(f"Fetching data from: {url}")
        try:
            response = self.session.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Network error occurred: {e}")
            return {}
