from aiohttp import ClientSession

class HTTPClient:
    def __init__(self, base_url: str, api_key: str):
        self._session = ClientSession(
            base_url=base_url
        )
        self._api_key = api_key
