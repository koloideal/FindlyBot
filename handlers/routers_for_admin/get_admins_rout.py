import typing
from database_func.admins_dao import ActionsOnAdmin
from aiogram.types import FSInputFile, Message
from datetime import datetime
import json
import os
from database_func.users_dao import ActionsOnUsers
import polib
from polib import POFile

if typing.TYPE_CHECKING:
    from _typeshed import SupportsWrite


en_msgs: POFile = polib.pofile("locales/en/get_admins_rout.po")
ru_msgs: POFile = polib.pofile("locales/ru/get_admins_rout.po")


async def get_admins_rout(message: Message) -> None:
    user_id: int = message.from_user.id
    user_config: dict = await ActionsOnUsers.get_all_configs(user_id=user_id)
    lang: str = user_config["language"]

    match lang:
        case "RU":
            msgs: POFile = ru_msgs
        case "EN":
            msgs: POFile = en_msgs
        case _:
            msgs: POFile = en_msgs

    all_admins: list[dict[str | int]] = await ActionsOnAdmin.get_admins(only_ids=False)

    if not all_admins:
        await message.answer(msgs.find("empty_database_msg").msgstr)
        return

    file_name: str = "secret_data/admin_users.json"

    with open(file_name, "w", encoding="utf8") as file:  # type: SupportsWrite[str]
        json.dump({'admins': all_admins}, file, indent=4, ensure_ascii=False)

    document: FSInputFile = FSInputFile(file_name)
    caption: str = msgs.find("caption_msg").msgstr.format(
        date=datetime.now().strftime("%d-%m-%Y")
    )
    await message.answer_document(document=document, caption=caption)
    os.remove(file_name)
