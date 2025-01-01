import os
import re
from os import path

import requests
from aiocache import cached
from aiocache.serializers import PickleSerializer

from database_func.actions_on_users import ActionsOnUsers
from utils.query_to_hash import req_to_hash


@cached(ttl=5 * 60, serializer=PickleSerializer())
async def api_data_to_dump(
    api_json_data: dict, requestor_id: int, query_path_hash
) -> dict:
    to_dump_data: dict = {}
    all_configs: dict = await ActionsOnUsers.get_all_configs(requestor_id)
    max_size: int = all_configs["max_size"]

    os.makedirs(f"local_data/images/{requestor_id}", exist_ok=True)

    for marketplace in api_json_data:
        os.makedirs(
            f"local_data/images/{requestor_id}/{query_path_hash}/{marketplace}",
            exist_ok=True,
        )
        items: list = []
        for k, item in enumerate(api_json_data[marketplace]):
            if k <= int(max_size):
                res_item = item
                res_item["id"] = k
                res_item["name"] = re.sub(r"[ /\\]", "_", item["name"])
                hash_name = await req_to_hash(res_item["name"])
                items.append(res_item)

                if res_item["image"] != "images/placeholder.png" and not path.isfile(
                    f"local_data/images/{requestor_id}/{query_path_hash}/{marketplace}/{hash_name}.jpg"
                ):
                    data = requests.get(res_item["image"])
                    with open(
                        f"local_data/images/{requestor_id}/{query_path_hash}/{marketplace}/{hash_name}.jpg",
                        "wb",
                    ) as f:
                        f.write(data.content)
            else:
                break
        to_dump_data[marketplace] = items

    return to_dump_data
