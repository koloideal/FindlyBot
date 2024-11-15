from typing import Any
from httpx import AsyncClient, Response
from utils.get_config import GetConfig


async def get_api_data(query: str,
                       max_size: int = None,
                       only_new: bool = None) -> Response | Any:

    api_url: str = GetConfig.get_api_config()["api_url"]
    api_url: str = api_url.format(query=query,
                                  max_size=max_size,
                                  only_new=1 if only_new else 0)

    async with AsyncClient(timeout=20) as client:
        api_data: Response = await client.get(api_url)

    return api_data
