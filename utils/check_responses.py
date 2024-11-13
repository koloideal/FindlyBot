import json
import os
import shutil


async def check_responses(user_id: int) -> bool:
    if os.path.exists(f"local_data/images/{user_id}/responses.json"):
        with open(f"local_data/images/{user_id}/responses.json", "r") as file:
            responses: list[dict[str]] = json.load(file)["responses"]
    else:
        return False

    if len(responses) < 5:
        return False
    else:
        oldest_response = min(responses, key=lambda x: x["date"])
        data = json.load(open(f"local_data/images/{user_id}/responses.json", "r"))
        data["responses"].remove(oldest_response)

        with open(f"local_data/images/{user_id}/responses.json", "w") as file:
            json.dump(data, file, indent=4)

        shutil.rmtree(
            f'local_data/images/{user_id}/{oldest_response['name']}', ignore_errors=True
        )
        os.remove(f'local_data/products_data/{user_id}/{oldest_response["name"]}.json')

        return True
