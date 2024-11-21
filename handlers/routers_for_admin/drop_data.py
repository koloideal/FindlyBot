from aiogram import types

from database_func.actions_on_users import ActionsOnUsers
from utils.del_data_dirs import del_data_dirs
from utils.make_dirs import make_dirs
from utils.get_config import GetConfig
import polib

en_msgs = polib.pofile('locales/en/drop_data.po')
ru_msgs = polib.pofile('locales/ru/drop_data.po')


async def drop_data_rout(message: types.Message) -> None:
    creator_id: int = GetConfig.get_bot_config()["Settings"]["creator_id"]
    user_id: int = message.from_user.id
    lang: str = await ActionsOnUsers.get_user_lang_config(user_id=user_id)

    match lang:
        case "RU":
            msgs = ru_msgs
        case "EN":
            msgs = en_msgs
        case _:
            msgs = en_msgs

    if user_id != creator_id:
        await message.answer(msgs.find('unknown_command_msg').msgstr)

    else:
        try:
            await del_data_dirs()
            await make_dirs()
        except FileNotFoundError:
            pass
        finally:
            await message.answer(msgs.find('hope_msg').msgstr)

    return
