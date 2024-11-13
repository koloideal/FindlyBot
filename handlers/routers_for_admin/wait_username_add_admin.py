from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils.get_config import GetConfig
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import UsernameInvalidError
from database_func.action_on_admin import ActionsOnAdmin
from telethon.helpers import TotalList


config: dict = GetConfig.get_bot_config()
api_id: str = config["Settings"]["api_id"]
api_hash: str = config["Settings"]["api_hash"]
creator_id: str = config["Settings"]["creator_id"]

client: TelegramClient = TelegramClient("session", int(api_id), api_hash)


async def get_username_for_add_admin_rout(message: Message, state: FSMContext) -> None:
    try:
        await client.start()

        if message.text.startswith("t.me/") or message.text.startswith("https://t.me/"):
            raise ValueError

        future_admin_username: str = (
            message.text if message.text[0] != "@" else message.text[1:]
        )

        user: TotalList = await client.get_participants(future_admin_username)

        if user[0].bot or len(user) != 1:
            raise ValueError

    except (UsernameInvalidError, ValueError):
        await message.answer("Invalid username")

    else:
        username: str = future_admin_username
        user_id: int = user[0].id
        first_name: str = user[0].first_name
        last_name: str = user[0].last_name

        await ActionsOnAdmin.add_admin(
            message=message,
            future_admin={
                "id": user_id,
                "first_name": first_name,
                "last_name": last_name,
                "username": username,
            },
        )

    finally:
        await client.disconnect()
        await state.clear()

    return
