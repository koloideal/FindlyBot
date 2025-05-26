import shutil
import os

from utils.query_to_hash import req_to_hash


async def del_user_searching_data(username: str) -> None:
    hash_username: str = await req_to_hash(username)
    images_path = f"local_data/images/{hash_username}"
    if os.path.isdir(images_path):
        shutil.rmtree(images_path, ignore_errors=True)

    products_data_path = f"local_data/products_data/{hash_username}"
    if os.path.isdir(products_data_path):
        shutil.rmtree(products_data_path, ignore_errors=True)
