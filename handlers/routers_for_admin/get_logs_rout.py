from logging import getLogger, Logger
from aiogram.types import Message
from aiogram.types import FSInputFile
from datetime import datetime
from aiogram.exceptions import TelegramBadRequest
from database_func.actions_on_users import ActionsOnUsers
import polib
from polib import POFile


en_msgs: POFile = polib.pofile("locales/en/get_logs_rout.po")
ru_msgs: POFile = polib.pofile("locales/ru/get_logs_rout.po")

action_logger: Logger = getLogger('action_logger')


async def get_logs_rout(message: Message) -> None:
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

    full_file_name: str = "secret_data/logs.log"
    document: FSInputFile = FSInputFile(full_file_name)
    captions: str = msgs.find("caption_msg").msgstr.format(
        date=datetime.now().strftime("%d-%m-%Y")
    )

    try:
        action_logger.warning("Bot logs have been successfully requested")
        await message.answer_document(document=document, caption=captions)
    except TelegramBadRequest:
        action_logger.warning("Bot logs have been unsuccessfully requested")
        await message.answer(msgs.find("empty_logs_msg").msgstr)
