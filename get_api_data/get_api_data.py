from logging import getLogger, Logger
from typing import Any
from httpx import AsyncClient, Response, ConnectTimeout
from utils.get_config import GetConfig


action_logger: Logger = getLogger('action_logger')
main_logger: Logger = getLogger('root')


async def get_api_data(
    query: str,
    max_size: int,
    only_new: str,
    price_filter: str,
    name_filter: str,
    exclusion_words: str = None,
) -> Response | bool:
    api_url: str = GetConfig.get_api_config()["api_url"]
    api_url: str = api_url.format(
        query=query,
        max_size=max_size,
        only_new=only_new,
        price_filter=price_filter,
        name_filter=name_filter,
    )

    if exclusion_words:
        api_url += f"&ew={exclusion_words}"

    async with AsyncClient(timeout=10) as client:
        try:
            api_data: Response = await client.get(api_url)
        except ConnectTimeout:
            main_logger.error("Unsuccessful API request, ConnectTimeout error was intercepted")
            action_logger.error("Unsuccessful API request, ConnectTimeout error was intercepted")
            return False
        else:
            main_logger.warning(f"Successful API request, url: $ {api_url} $")
            action_logger.warning(f"Successful API request, url: $ {api_url} $")
            return api_data
