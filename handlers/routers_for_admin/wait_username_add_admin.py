from typing import Any
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from database_func.database_models import Admin, UserConfig
from database_func.users_config_dao import UsersConfigDAO
from utils.get_config import GetConfig
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import UsernameInvalidError, UsernameOccupiedError
from database_func.admins_dao import AdminsDAO
from telethon.helpers import TotalList
from exceptions.users_exceptions import InvalidUsernameForAddAdmin
import polib
from polib import POFile


en_msgs: POFile = polib.pofile("locales/en/wait_username_add_admin.po")
ru_msgs: POFile = polib.pofile("locales/ru/wait_username_add_admin.po")


config: dict = GetConfig.get_bot_config()
api_id: str = config["Settings"]["api_id"]
api_hash: str = config["Settings"]["api_hash"]
creator_id: str = config["Settings"]["creator_id"]

client: TelegramClient = TelegramClient("session", int(api_id), api_hash)


async def get_username_for_add_admin_rout(message: Message, state: FSMContext) -> None:
    from main import bot
    raw_input_username: str = message.text
    try:
        await client.start()
        if raw_input_username.startswith("t.me/") or raw_input_username.startswith("https://t.me/"):
            raise InvalidUsernameForAddAdmin(raw_input_username)

        finished_input_username: str = (
            raw_input_username
            if raw_input_username[0] != "@"
            else raw_input_username[1:]
        )

        admin: TotalList = await client.get_participants(finished_input_username)
        admin: Any | Admin = admin[0]
        admin_id = admin.user_id

        if admin.bot or len(admin) != 1:
            raise InvalidUsernameForAddAdmin(raw_input_username)

    except (UsernameInvalidError, UsernameOccupiedError, ValueError, InvalidUsernameForAddAdmin):
        await message.answer(en_msgs.find("invalid_username_msg").msgstr)

    else:

        AdminsDAO().add_admin(admin=admin)
        user_config: UsersConfigDAO = UsersConfigDAO()

        my_id: int = message.from_user.id
        my_config: UserConfig = user_config.get_all_configs(user_id=my_id)
        language: str = my_config.language

        params: dict[str, str | int] = UserConfig.get_default_user_config(admin_id)

        user_config.config_user_to_database(params=params)
        new_admin_config: UserConfig = user_config.get_all_configs(user_id=admin_id)
        new_admin_lang: str = new_admin_config.language

        match language:
            case "RU":
                msgs: POFile = ru_msgs
            case "EN":
                msgs: POFile = en_msgs
            case _:
                msgs: POFile = en_msgs

        match new_admin_lang:
            case "RU":
                new_admin_msgs: POFile = ru_msgs
            case "EN":
                new_admin_msgs: POFile = en_msgs
            case _:
                new_admin_msgs: POFile = en_msgs
        try:
            async with bot.session:
                await bot.send_message(admin_id, new_admin_msgs.find("congratulations_msg").msgstr)
        except TelegramForbiddenError:
            await message.answer(msgs.find("blocked_bot_msg").msgstr.format(
                    finished_input_username=finished_input_username
                )
            )
        except TelegramBadRequest:
            pass

        await message.answer(
            msgs.find("new_admin_msg").msgstr.format(
                finished_input_username=finished_input_username
            )
        )

    finally:
        await client.disconnect()
        await state.clear()
