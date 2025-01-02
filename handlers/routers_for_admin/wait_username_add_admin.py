from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from database_func.actions_on_users import ActionsOnUsers
from utils.get_config import GetConfig
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import UsernameInvalidError, UsernameOccupiedError
from database_func.action_on_admin import ActionsOnAdmin
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
    raw_input_username: str = message.text
    try:
        await client.start()

        if raw_input_username.startswith("t.me/") or raw_input_username.startswith(
            "https://t.me/"
        ):
            raise InvalidUsernameForAddAdmin(raw_input_username)

        finished_input_username: str = (
            raw_input_username
            if raw_input_username[0] != "@"
            else raw_input_username[1:]
        )

        user: TotalList = await client.get_participants(finished_input_username)

        if user[0].bot or len(user) != 1:
            raise InvalidUsernameForAddAdmin(raw_input_username)

    except (UsernameInvalidError, UsernameOccupiedError, ValueError, InvalidUsernameForAddAdmin):
        await message.answer(en_msgs.find("invalid_username_msg").msgstr)

    else:
        user_id, username, first_name, last_name = (
            user[0].id,
            user[0].username,
            user[0].first_name,
            user[0].last_name,
        )

        await ActionsOnAdmin.add_admin(
            future_admin={
                "id": user_id,
                "first_name": first_name,
                "last_name": last_name,
                "username": username,
            },
        )
        my_id: int = message.from_user.id
        user_config: dict = await ActionsOnUsers.get_all_configs(user_id=my_id)
        lang: str = user_config["language"]

        match lang:
            case "RU":
                msgs: POFile = ru_msgs
            case "EN":
                msgs: POFile = en_msgs
            case _:
                msgs: POFile = en_msgs
        await message.answer(
            msgs.find("new_admin_msg").msgstr.format(
                finished_input_username=finished_input_username
            )
        )

    finally:
        client.disconnect()
        await state.clear()
