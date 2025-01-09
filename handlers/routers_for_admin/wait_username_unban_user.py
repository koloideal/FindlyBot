from logging import Logger, getLogger

from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils.get_config import GetConfig
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import UsernameInvalidError, UsernameNotOccupiedError
from database_func.users_dao import ActionsOnUsers
from telethon.helpers import TotalList
import polib
from polib import POFile


en_msgs: POFile = polib.pofile("locales/en/wait_username_unban_user.po")
ru_msgs: POFile = polib.pofile("locales/ru/wait_username_unban_user.po")

config: dict = GetConfig.get_bot_config()
api_id: str = config["Settings"]["api_id"]
api_hash: str = config["Settings"]["api_hash"]

client: TelegramClient = TelegramClient("session", int(api_id), api_hash)

action_logger: Logger = getLogger('action_logger')


async def get_username_for_unban_user_rout(message: Message, state: FSMContext) -> None:
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
    raw_input_username: str = message.text
    finished_input_username: str = (
        raw_input_username if raw_input_username[0] != "@" else raw_input_username[1:]
    )
    try:
        await client.start()

        if raw_input_username.startswith("t.me/") or raw_input_username.startswith(
            "https://t.me/"
        ):
            raise UsernameInvalidError

        user: TotalList = await client.get_participants(finished_input_username)
        user_id, username, first_name, last_name = (
            user[0].id,
            user[0].username,
            user[0].first_name,
            user[0].last_name,
        )

        if len(user) != 1:
            raise UsernameInvalidError

    except (UsernameInvalidError, ValueError, UsernameNotOccupiedError):
        await message.answer(msgs.find("invalid_username_msg").msgstr)

    else:
        is_banned: bool = await ActionsOnUsers.unban_user(
            ex_ban_user={
                "id": user_id,
                "first_name": first_name,
                "last_name": last_name,
                "username": username,
            },
        )

        if is_banned:
            await message.answer(
                msgs.find("user_unban_msg").msgstr.format(
                    finished_input_username=finished_input_username
                )
            )
        else:
            action_logger.warning(f"User $ @{username} $ unbanned by admin $ {user_id} $")
            await message.answer(
                msgs.find("user_not_ban_msg").msgstr.format(
                    finished_input_username=finished_input_username
                )
            )

    finally:
        await client.disconnect()
        await state.clear()
