from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from polib import POFile
from database_func.users_dao import ActionsOnUsers
from utils.get_config import GetConfig
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import UsernameInvalidError
from database_func.admins_dao import ActionsOnAdmin
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
    user_config: dict = await ActionsOnUsers.get_all_configs(user_id=admin_id)
    lang: str = user_config["language"]

    match lang:
        case "RU":
            msgs: POFile = ru_msgs
        case "EN":
            msgs: POFile = en_msgs
        case _:
            msgs: POFile = en_msgs
    try:
        admin_ids: list[int] = await ActionsOnAdmin.get_admins(only_ids=True)
        await client.start()

        if message.text.startswith("t.me/") or message.text.startswith("https://t.me/"):
            raise ValueError

        ex_admin_username: str = (
            message.text if message.text[0] != "@" else message.text[1:]
        )

        user: TotalList = await client.get_participants(ex_admin_username)

        admin_id: int = user[0].id
        admin_username: str = user[0].username

        if len(user) != 1:
            raise ValueError

        if admin_id not in admin_ids:
            raise TypeError

    except (UsernameInvalidError, ValueError):
        await message.answer(msgs.find("invalid_username_msg").msgstr)

    except TypeError:
        await message.answer(msgs.find("not_admin_msg").msgstr)

    else:
        await ActionsOnAdmin.del_admin(
            ex_admin={"id": admin_id, "username": admin_username},
        )
        await message.answer(
            msgs.find("admin_del_msg").msgstr.format(admin_username=admin_username)
        )

    finally:
        client.disconnect()
        await state.clear()
