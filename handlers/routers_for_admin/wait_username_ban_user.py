from aiogram import types
from aiogram.fsm.context import FSMContext
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import UsernameInvalidError
from database_func.actions_on_users import ActionsOnUsers
from database_func.action_on_admin import ActionsOnAdmin
from telethon.helpers import TotalList
from utils.get_config import GetConfig


config: dict = GetConfig.get_bot_config()
api_id: str = config["Settings"]["api_id"]
api_hash: str = config["Settings"]["api_hash"]
creator_id: int = config["Settings"]["creator_id"]

client: TelegramClient = TelegramClient("session", int(api_id), api_hash)


async def get_username_for_ban_user_rout(
    message: types.Message, state: FSMContext
) -> None:
    try:
        await client.start()

        if message.text.startswith("t.me/") or message.text.startswith("https://t.me/"):
            raise ValueError

        future_ban_user_username: str = (
            message.text if message.text[0] != "@" else message.text[1:]
        )

        user: TotalList = await client.get_participants(future_ban_user_username)

        user_id: int = user[0].id
        user_username: str = user[0].username
        user_first_name: str = user[0].first_name
        user_last_name: str = user[0].last_name

        admins_id: list = await ActionsOnAdmin.get_admins()

        if (
            (user_id in admins_id) or (user_id == creator_id)
        ) and message.from_user.id != creator_id:
            raise TypeError

        if len(user) != 1:
            raise ValueError

    except (UsernameInvalidError, ValueError):
        await message.answer("Invalid username")

    except TypeError:
        await message.answer("You can't ban the admin or the Creator")

    else:
        if user_id in admins_id:
            await ActionsOnAdmin.del_admin(
                message=message,
                ex_admin={"id": user_id,
                          "username": user_username},
            )

        await ActionsOnUsers.ban_user(
            message=message,
            future_ban_user={
                "id": user_id,
                "first_name": user_first_name,
                "last_name": user_last_name,
                "username": user_username,
            },
        )

    finally:
        await client.disconnect()
        await state.clear()

    return
