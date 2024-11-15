import logging
import os
import re
import time
import polib
from ..search_command_funcs.api_data_to_dump import api_data_to_dump
from ..search_command_funcs.forming_response import forming_response
from aiogram.types import Message
from database_func.actions_on_users import ActionsOnUsers
from aiogram.fsm.context import FSMContext
from httpx import Response, HTTPError
from get_api_data.get_api_data import get_api_data
from utils.query_to_hash import req_to_hash
import json


en_msgs = polib.pofile('locales/en/wait_query_to_search.po')
ru_msgs = polib.pofile('locales/ru/wait_query_to_search.po')


async def get_query_to_search_rout(message: Message, state: FSMContext) -> None:
    query_with_plus: str = re.sub(r" ", "+", message.text.strip())
    requestor_id = message.from_user.id
    query_hash = await req_to_hash(query_with_plus)
    wait_message: Message = await message.answer(en_msgs.find('search_in_progress'))

    os.makedirs(f"local_data/products_data/{requestor_id}", exist_ok=True)
    os.makedirs(f"local_data/images/{requestor_id}", exist_ok=True)

    max_size: int = await ActionsOnUsers.get_user_max_size_config(requestor_id)
    only_new: bool = await ActionsOnUsers.get_user_only_new_config(requestor_id)

    try:
        api_data: Response = await get_api_data(
            query_with_plus, max_size=max_size, only_new=only_new
        )
        api_json_data = api_data.json()["data"]
        if not api_json_data:
            await message.answer(en_msgs.find('empty_response'))
            await state.clear()
            return
        else:
            current_response = {"name": query_hash, "date": time.time()}
            if os.path.exists(f"local_data/images/{requestor_id}/responses.json"):
                data = json.load(
                    open(f"local_data/images/{requestor_id}/responses.json")
                )
                data["responses"].append(current_response)
                with open(
                    f"local_data/images/{requestor_id}/responses.json", "w"
                ) as file:
                    json.dump(data, file, indent=4)
            else:
                with open(
                    f"local_data/images/{requestor_id}/responses.json", "w"
                ) as file:
                    data = {"responses": [current_response]}
                    json.dump(data, file, indent=4)

            to_dump_data: dict = await api_data_to_dump(
                api_json_data, requestor_id, query_hash
            )

            with open(
                f"local_data/products_data/{requestor_id}/{query_hash}.json", "w"
            ) as file:
                json.dump(to_dump_data, file, indent=4, ensure_ascii=False)

    except HTTPError as e:
        logging.error(e, exc_info=True)
    else:
        await forming_response(message, query_with_plus, wait_message)
    finally:
        await state.clear()
