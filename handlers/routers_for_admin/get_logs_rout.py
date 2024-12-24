from aiogram.types import Message
from database_func.action_on_admin import ActionsOnAdmin
from aiogram.types import FSInputFile
from datetime import datetime
from aiogram.exceptions import TelegramBadRequest
from database_func.actions_on_users import ActionsOnUsers
from utils.get_config import GetConfig
import polib
from polib import POFile


en_msgs: POFile = polib.pofile('locales/en/get_logs_rout.po')
ru_msgs: POFile = polib.pofile('locales/ru/get_logs_rout.po')


async def get_logs_rout(message: Message) -> None:
    creator_id: int = GetConfig.get_bot_config()["Settings"]["creator_id"]
    user_id: int = message.from_user.id
    user_config: dict = await ActionsOnUsers.get_all_configs(user_id=user_id)
    lang: str = user_config['language']

    match lang:
        case "RU":
            msgs: POFile = ru_msgs
        case "EN":
            msgs: POFile = en_msgs
        case _:
            msgs: POFile = en_msgs

    admins_id: list[int] = await ActionsOnAdmin.get_admins()

    if (user_id != creator_id) and (user_id not in admins_id):
        await message.answer(msgs.find('unknown_command_msg').msgstr)

    else:
        full_file_name: str = "secret_data/logs.log"
        document: FSInputFile = FSInputFile(full_file_name)
        captions: str = msgs.find('caption_msg').msgstr.format(date=datetime.now().strftime("%d-%m-%Y"))

        try:
            await message.answer_document(
                document=document,
                caption=captions
            )
        except TelegramBadRequest:
            await message.answer(msgs.find('empty_logs_msg').msgstr)
