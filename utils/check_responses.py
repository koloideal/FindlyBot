import json
import os
import shutil
from _typeshed import SupportsWrite, SupportsRead

from utils.query_to_hash import req_to_hash


async def check_responses(username: str) -> bool:
    hash_username: str = await req_to_hash(username)
    if os.path.exists(f"local_data/images/{hash_username}/responses.json"):
        with open(f"local_data/images/{hash_username}/responses.json", "r") as file: # type: SupportsRead[str | bytes]
            responses: list[dict[str]] = json.load(file)["responses"]
    else:
        return False

    if len(responses) < 5:
        return False
    else:
        oldest_response = min(responses, key=lambda x: x["date"])
        data = json.load(open(f"local_data/images/{hash_username}/responses.json", "r"))
        data["responses"].remove(oldest_response)

        with open(f"local_data/images/{hash_username}/responses.json", "w") as file: # type: SupportsWrite[str]
            json.dump(data, file, indent=4)

        shutil.rmtree(f'local_data/images/{hash_username}/{oldest_response['name']}', ignore_errors=True)
        os.remove(f'local_data/products_data/{hash_username}/{oldest_response["name"]}.json')

        return True
