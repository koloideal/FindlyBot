from typing import Any
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from polib import POFile
from database_func.database_models import UserConfig, Admin
from database_func.users_config_dao import UsersConfigDAO
from utils.get_config import GetConfig
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import UsernameInvalidError
from database_func.admins_dao import AdminsDAO
from telethon.helpers import TotalList
import polib


en_msgs: POFile = polib.pofile("locales/en/wait_username_del_admin.po")
ru_msgs: POFile = polib.pofile("locales/ru/wait_username_del_admin.po")


config: dict = GetConfig.get_bot_config()
api_id: str = config["Settings"]["api_id"]
api_hash: str = config["Settings"]["api_hash"]

client: TelegramClient = TelegramClient("session", int(api_id), api_hash)


async def get_username_for_del_admin_rout(message: Message, state: FSMContext) -> None:
    admin_id: int = message.from_user.id
    user_config: UserConfig = UsersConfigDAO().get_all_configs(user_id=admin_id)
    language: str = user_config.language

    match language:
        case "RU":
            msgs: POFile = ru_msgs
        case "EN":
            msgs: POFile = en_msgs
        case _:
            msgs: POFile = en_msgs
    try:
        admins: list[Admin] = AdminsDAO().get_admins()
        admin_ids: list[int] = [admin.user_id for admin in admins]

        await client.start()

        if message.text.startswith("t.me/") or message.text.startswith("https://t.me/"):
            raise ValueError

        ex_admin_username: str = (
            message.text if message.text[0] != "@" else message.text[1:]
        )

        user: TotalList = await client.get_participants(ex_admin_username)
        ex_admin: Any = user[0]

        admin_id: int = ex_admin.id
        admin_username: str = ex_admin.username

        if len(user) != 1:
            raise ValueError

        if admin_id not in admin_ids:
            raise TypeError

    except (UsernameInvalidError, ValueError):
        await message.answer(msgs.find("invalid_username_msg").msgstr)

    except TypeError:
        await message.answer(msgs.find("not_admin_msg").msgstr)

    else:
        AdminsDAO().del_admin(admin_id=admin_id)

        await message.answer(
            msgs.find("admin_del_msg").msgstr.format(admin_username=admin_username)
        )

    finally:
        client.disconnect()
        await state.clear()
