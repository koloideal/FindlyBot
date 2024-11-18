from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils.get_config import GetConfig
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import UsernameInvalidError
from database_func.actions_on_users import ActionsOnUsers
from telethon.helpers import TotalList
from exceptions.users_exceptions import InvalidUsernameForUnban
import polib


en_msgs = polib.pofile('locales/en/wait_username_unban_user.po')
ru_msgs = polib.pofile('locales/ru/wait_username_unban_user.po')


config: dict = GetConfig.get_bot_config()
api_id: str = config["Settings"]["api_id"]
api_hash: str = config["Settings"]["api_hash"]

client: TelegramClient = TelegramClient("session", int(api_id), api_hash)


async def get_username_for_unban_user_rout(message: Message,
                                           state: FSMContext) -> None:
    raw_input_username = message.text
    finished_input_username: str = raw_input_username if raw_input_username[0] != "@" else raw_input_username[1:]
    try:
        client.start()

        if raw_input_username.startswith("t.me/") or raw_input_username.startswith("https://t.me/"):
            raise InvalidUsernameForUnban(raw_input_username)

        user: TotalList = await client.get_participants(finished_input_username)
        user_id, user_username, user_first_name, user_last_name = \
            user[0].id, user[0].username, user[0].first_name, user[0].last_name

        if len(user) != 1:
            raise InvalidUsernameForUnban(raw_input_username)

    except UsernameInvalidError:
        raise InvalidUsernameForUnban(raw_input_username)

    except InvalidUsernameForUnban:
        await message.answer(en_msgs.find("invalid_username_msg"))

    else:
        is_banned = await ActionsOnUsers.unban_user(
            ex_ban_user={
                "id": user_id,
                "first_name": user_first_name,
                "last_name": user_last_name,
                "username": user_username,
            },
        )

        if is_banned:
            await message.answer(en_msgs.find("user_unban_msg").format(finished_input_username=finished_input_username))
        else:
            await message.answer(en_msgs.find("user_not_ban_msg").format(finished_input_username=finished_input_username))

    finally:
        await client.disconnect()
        await state.clear()
