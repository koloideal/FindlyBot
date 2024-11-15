from database_func.action_on_admin import ActionsOnAdmin
from aiogram.types import FSInputFile, Message
from datetime import datetime
import json
import os
from utils.get_config import GetConfig
import polib


en_msgs = polib.pofile('locales/en/get_admins_rout.po')


async def get_admins_rout(message: Message) -> None:
    creator_id: int = GetConfig.get_bot_config()["Settings"]["creator_id"]
    user_id: int = message.from_user.id

    admins_id: list = await ActionsOnAdmin.get_admins()

    if user_id != creator_id and user_id not in admins_id:
        await message.answer(en_msgs.find('unknown_command_msg'))

    else:
        all_admins: list = await ActionsOnAdmin.get_admins(False)

        if not all_admins:
            await message.answer(en_msgs.find('empty_database_msg'))
            return

        to_dump_data: dict = {}

        for admin in all_admins:
            to_dump_data[admin[3]]: dict = {
                "admin_id": admin[0],
                "admin_first_name": admin[1],
                "admin_last_name": admin[2],
                "admin_username": admin[3],
            }

        full_file_name: str = "secret_data/admin_users.json"

        with open(full_file_name, "w", encoding="utf8") as file:
            json.dump(to_dump_data, file, indent=4, ensure_ascii=False)

        document: FSInputFile = FSInputFile(full_file_name)
        caption: str = en_msgs.find('caption_msg').format(date=datetime.now().strftime("%d-%m-%Y"))

        await message.answer_document(
            document=document,
            caption=caption
        )

        os.remove(full_file_name)

    return
