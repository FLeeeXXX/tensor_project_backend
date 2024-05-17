from fastapi_cache.decorator import cache
from app.http_client.base import HTTPClient
from app.exceptions import ServerNetworkException


class OpenWeatherHTTPClient(HTTPClient):
    @cache(expire=120)
    async def get_weather(self, lat: str, lon: str):
        try:
            async with self._session.get(
                    f'/data/2.5/forecast?lat={lat}&lon={lon}&appid={self._api_key}&lang=ru&units=metric') as response:
                result = await response.json()
                return result
        except:
            raise ServerNetworkException
        finally:
            await self._session.close()
            