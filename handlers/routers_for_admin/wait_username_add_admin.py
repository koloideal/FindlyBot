from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils.get_config import GetConfig
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import UsernameInvalidError
from database_func.action_on_admin import ActionsOnAdmin
from telethon.helpers import TotalList
from exceptions.users_exceptions import InvalidUsernameForAddAdmin


config: dict = GetConfig.get_bot_config()
api_id: str = config["Settings"]["api_id"]
api_hash: str = config["Settings"]["api_hash"]
creator_id: str = config["Settings"]["creator_id"]

client: TelegramClient = TelegramClient("session", int(api_id), api_hash)


async def get_username_for_add_admin_rout(message: Message, state: FSMContext) -> None:
    raw_input_username: str = message.text
    try:
        client.start()

        if raw_input_username.startswith("t.me/") or raw_input_username.startswith("https://t.me/"):
            raise InvalidUsernameForAddAdmin(raw_input_username)

        finished_input_username: str = raw_input_username if raw_input_username[0] != "@" else raw_input_username[1:]

        user: TotalList = await client.get_participants(finished_input_username)

        if user[0].bot or len(user) != 1:
            raise InvalidUsernameForAddAdmin(raw_input_username)

    except UsernameInvalidError:
        raise InvalidUsernameForAddAdmin(raw_input_username)

    except InvalidUsernameForAddAdmin:
        await message.answer("Invalid username for add admin")

    else:
        user_id, username, first_name, last_name = \
            user[0].id, user[0].username, user[0].first_name, user[0].last_name

        await ActionsOnAdmin.add_admin(
            future_admin={
                "id": user_id,
                "first_name": first_name,
                "last_name": last_name,
                "username": username,
            },
        )
        await message.answer(f"@{finished_input_username} is now an admin or already was")

    finally:
        client.disconnect()
        await state.clear()
