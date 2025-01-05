from logging import Logger, getLogger
import os
import re
import time
import typing
import polib
from exceptions.request_exceptions import TooLongQueryForSearchError
from ..search_command_funcs.api_data_to_dump import api_data_to_dump
from ..search_command_funcs.forming_response import forming_response
from aiogram.types import Message
from database_func.actions_on_users import ActionsOnUsers
from aiogram.fsm.context import FSMContext
from httpx import Response, HTTPError
from get_api_data.get_api_data import get_api_data
from utils.query_to_hash import req_to_hash
import json
if typing.TYPE_CHECKING:
    from _typeshed import SupportsWrite


en_msgs = polib.pofile("locales/en/wait_query_to_search.po")
ru_msgs = polib.pofile("locales/ru/wait_query_to_search.po")

main_logger: Logger = getLogger('main_logger')
action_logger: Logger = getLogger('action_logger')


async def get_query_to_search_rout(message: Message, state: FSMContext) -> None:
    query: str = message.text.strip()
    requestor_id = message.from_user.id
    try:
        if len(query) > 25:
            raise TooLongQueryForSearchError(len(query))
        query_with_plus: str = re.sub(r" ", "+", query)
        user_config: dict = await ActionsOnUsers.get_all_configs(user_id=requestor_id)
        lang: str = user_config["language"]

        match lang:
            case "RU":
                msgs = ru_msgs
            case "EN":
                msgs = en_msgs
            case _:
                msgs = en_msgs
        wait_message: Message = await message.answer(msgs.find("search_in_progress").msgstr)

        os.makedirs(f"local_data/products_data/{requestor_id}", exist_ok=True)
        os.makedirs(f"local_data/images/{requestor_id}", exist_ok=True)

        max_size: int = user_config["max_size"]
        only_new: str = user_config["only_new"]
        price_filter: str = user_config["price_filter"]
        name_filter: str = user_config["name_filter"]


        api_data: Response = await get_api_data(
            query_with_plus,
            max_size=max_size,
            only_new=only_new,
            price_filter=price_filter,
            name_filter=name_filter
        )
        api_data_to_json = api_data.json()

        products_data: dict[str, dict] = api_data_to_json["products_data"]
        metadata: dict[str | dict] = api_data_to_json["request_metadata"]

        action_logger.warning(f"Request from $ {requestor_id} $ with $ {metadata['size_of_products']['all']} $ products")

        raw_query_path: str = metadata["request_url"]
        query_path = raw_query_path[raw_query_path.find("?") :]
        query_path_hash = await req_to_hash(query_path)

        if not products_data:
            await message.answer(msgs.find("empty_response").msgstr)
            await state.clear()
            return
        else:
            current_response = {"name": query_path_hash, "date": time.time()}
            if os.path.exists(f"local_data/images/{requestor_id}/responses.json"):
                data = json.load(open(f"local_data/images/{requestor_id}/responses.json"))
                data["responses"].append(current_response)
                with open(
                    f"local_data/images/{requestor_id}/responses.json", "w"
                ) as file: # type: SupportsWrite[str]
                    json.dump(data, file, indent=4)
            else:
                with open(
                    f"local_data/images/{requestor_id}/responses.json", "w"
                ) as file: # type: SupportsWrite[str]
                    data = {"responses": [current_response]}
                    json.dump(data, file, indent=4)

            to_dump_data: dict = await api_data_to_dump(
                products_data, requestor_id, query_path_hash
            )

            with open(
                f"local_data/products_data/{requestor_id}/{query_path_hash}.json", "w"
            ) as file: # type: SupportsWrite[str]
                json.dump(to_dump_data, file, indent=4, ensure_ascii=False)

    except HTTPError as e:
        main_logger.error(e, exc_info=True)
    except TooLongQueryForSearchError as e:
        action_logger.error(f"{e} from user {requestor_id}")
        await message.answer(str(e))
    else:
        await forming_response(
            message=message,
            query_path_hash=query_path_hash,
            query=metadata["request_args"]["query"],
            wait_message=wait_message,
        )
    finally:
        await state.clear()
