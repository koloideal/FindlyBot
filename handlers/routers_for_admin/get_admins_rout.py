from _typeshed import SupportsWrite
from database_func.action_on_admin import ActionsOnAdmin
from aiogram.types import FSInputFile, Message
from datetime import datetime
import json
import os
from database_func.actions_on_users import ActionsOnUsers
from utils.get_config import GetConfig
import polib
from polib import POFile


en_msgs: POFile = polib.pofile('locales/en/get_admins_rout.po')
ru_msgs: POFile = polib.pofile('locales/ru/get_admins_rout.po')


async def get_admins_rout(message: Message) -> None:
    creator_id: int = GetConfig.get_bot_config()["Settings"]["creator_id"]
    user_id: int = message.from_user.id
    lang: str = await ActionsOnUsers.get_user_lang_config(user_id=user_id)

    match lang:
        case "RU":
            msgs: POFile = ru_msgs
        case "EN":
            msgs: POFile = en_msgs
        case _:
            msgs: POFile = en_msgs

    admins_id: list[int] = await ActionsOnAdmin.get_admins()

    if user_id != creator_id and user_id not in admins_id:
        await message.answer(msgs.find('unknown_command_msg').msgstr)

    else:
        all_admins: list[tuple] = await ActionsOnAdmin.get_admins(False)

        if not all_admins:
            await message.answer(msgs.find('empty_database_msg').msgstr)
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

        with open(full_file_name, "w", encoding="utf8") as file: # type: SupportsWrite[str]
            json.dump(to_dump_data, file, indent=4, ensure_ascii=False)

        document: FSInputFile = FSInputFile(full_file_name)
        caption: str = msgs.find('caption_msg').msgstr.format(date=datetime.now().strftime("%d-%m-%Y"))

        await message.answer_document(
            document=document,
            caption=caption
        )

        os.remove(full_file_name)
