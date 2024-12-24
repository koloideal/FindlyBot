from aiogram.types import Message
from polib import POFile
from database_func.actions_on_users import ActionsOnUsers
from utils.del_data_dirs import del_data_dirs
from utils.make_dirs import make_dirs
from utils.get_config import GetConfig
import polib

en_msgs: POFile = polib.pofile('locales/en/drop_data.po')
ru_msgs: POFile = polib.pofile('locales/ru/drop_data.po')


async def drop_data_rout(message: Message) -> None:
    creator_id: int = GetConfig.get_bot_config()["Settings"]["creator_id"]
    user_id: int = message.from_user.id
    user_config: dict = await ActionsOnUsers.get_all_configs(user_id=user_id)
    lang: str = user_config['language']

    match lang:
        case "RU":
            msgs: POFile = ru_msgs
        case "EN":
            msgs: POFile = en_msgs
        case _:
            msgs: POFile = en_msgs

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
