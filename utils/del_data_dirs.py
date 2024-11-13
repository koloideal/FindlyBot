import shutil
import os


async def del_data_dirs() -> None:
    paths = ["database", "local_data/products_data"]
    folders = [
        f"local_data/images/{e}"
        for e in os.listdir("local_data/images")
        if os.path.isdir(f"local_data/images/{e}")
    ]
    paths.extend(folders)

    for path in paths:
        shutil.rmtree(path, ignore_errors=True)
