from aiogram import types
from database_func.action_on_admin import ActionsOnAdmin
from aiogram.types import FSInputFile
from datetime import datetime
from aiogram.exceptions import TelegramBadRequest
from utils.get_config import GetConfig
import polib


en_msgs = polib.pofile('locales/en/get_logs_rout.po')


async def get_logs_rout(message: types.Message) -> None:
    creator_id: int = GetConfig.get_bot_config()["Settings"]["creator_id"]
    user_id: int = message.from_user.id

    admins_id: list = await ActionsOnAdmin.get_admins()

    if user_id != creator_id and user_id not in admins_id:
        await message.answer(en_msgs.find('unknown_command_msg'))

    else:
        full_file_name: str = "secret_data/logs.log"
        document: FSInputFile = FSInputFile(full_file_name)
        captions: str = en_msgs.find('caption_msg').format(date=datetime.now().strftime("%d-%m-%Y"))

        try:
            await message.answer_document(
                document=document,
                caption=captions
            )

        except TelegramBadRequest:
            await message.answer(en_msgs.find('empty_logs_msg'))

    return
