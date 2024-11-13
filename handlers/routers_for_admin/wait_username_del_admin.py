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

client: TelegramClient = TelegramClient("session", int(api_id), api_hash)


async def get_username_for_del_admin_rout(message: Message, state: FSMContext) -> None:
    try:
        admin_id: list = await ActionsOnAdmin.get_admins()

        await client.start()

        if message.text.startswith("t.me/") or message.text.startswith("https://t.me/"):
            raise ValueError

        ex_admin_username: str = (
            message.text if message.text[0] != "@" else message.text[1:]
        )

        user: TotalList = await client.get_participants(ex_admin_username)

        user_id: int = user[0].id
        user_username: str = user[0].username

        if len(user) != 1:
            raise ValueError

        if user_id not in admin_id:
            raise TypeError

    except (UsernameInvalidError, ValueError):
        await message.answer("Invalid username")

    except TypeError:
        await message.answer("The person is not an admin")

    else:
        await ActionsOnAdmin.del_admin(
            message=message,
            ex_admin={"id": user_id, "username": user_username},
        )

    finally:
        await client.disconnect()

        await state.clear()

    return
