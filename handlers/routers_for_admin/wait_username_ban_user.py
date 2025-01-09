from logging import Logger, getLogger

from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import UsernameInvalidError
from telethon.helpers import TotalList
import polib
from polib import POFile

from database_func.users_dao import ActionsOnUsers
from database_func.admins_dao import ActionsOnAdmin
from utils.get_config import GetConfig
from utils.del_user_searching_data import del_user_searching_data
from exceptions.users_exceptions import (
    InvalidUsernameForBan,
    AttemptToBanAdminOrCreator,
)


en_msgs: POFile = polib.pofile("locales/en/wait_username_ban_user.po")
ru_msgs: POFile = polib.pofile("locales/ru/wait_username_ban_user.po")

config: dict = GetConfig.get_bot_config()
api_id: str = config["Settings"]["api_id"]
api_hash: str = config["Settings"]["api_hash"]
creator_id: int = config["Settings"]["creator_id"]

client: TelegramClient = TelegramClient("session", int(api_id), api_hash)

action_logger: Logger = getLogger('action_logger')


async def get_username_for_ban_user_rout(message: Message, state: FSMContext) -> None:
    raw_input_username: str = message.text.strip()
    admin_id: int = message.from_user.id
    user_config: dict = await ActionsOnUsers.get_all_configs(user_id=admin_id)
    lang: str = user_config["language"]

    finished_input_username: str = (
        raw_input_username
        if raw_input_username[0] != "@"
        else raw_input_username[1:]
    )

    match lang:
        case "RU":
            msgs: POFile = ru_msgs
        case "EN":
            msgs: POFile = en_msgs
        case _:
            msgs: POFile = en_msgs
    admins_id: list[int] = await ActionsOnAdmin.get_admins()
    try:
        await client.start()

        if raw_input_username.startswith("t.me/") or raw_input_username.startswith(
            "https://t.me/"
        ):
            raise InvalidUsernameForBan(raw_input_username)

        user: TotalList = await client.get_participants(finished_input_username)
        user_id, username, first_name, last_name = (
            user[0].id,
            user[0].username,
            user[0].first_name,
            user[0].last_name,
        )

        if (
            (user_id in admins_id) or (user_id == creator_id)
        ) and admin_id != creator_id:
            raise AttemptToBanAdminOrCreator(finished_input_username)

        if len(user) != 1:
            raise InvalidUsernameForBan(raw_input_username)

    except AttemptToBanAdminOrCreator:
        action_logger.critical(f"Admin $ {admin_id} $ tried to block admin or creator $ @{finished_input_username} $")
        await message.answer(msgs.find("attempt_to_ban_admin_msg").msgstr)

    except (InvalidUsernameForBan, UsernameInvalidError, ValueError):
        action_logger.warning(f"Incorrect username $ @{finished_input_username} $ when trying to ban by admin $ {admin_id} $")
        await message.answer(msgs.find("invalid_username_msg").msgstr)

    else:
        await del_user_searching_data(user_id)
        if user_id in admins_id:
            await ActionsOnAdmin.del_admin(
                ex_admin={"id": user_id, "username": username},
            )
            await message.answer(
                msgs.find("del_admin_msg").msgstr.format(
                    finished_input_username=finished_input_username
                )
            )
        await ActionsOnUsers.ban_user(
            future_ban_user={
                "id": user_id,
                "first_name": first_name,
                "last_name": last_name,
                "username": username,
            },
        )
        action_logger.warning(f"User $ @{finished_input_username} $ banned by admin $ {admin_id} $")
        await message.answer(
            msgs.find("user_banned_msg").msgstr.format(
                finished_input_username=finished_input_username
            )
        )

    finally:
        client.disconnect()
        await state.clear()
