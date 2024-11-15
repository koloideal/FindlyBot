from aiogram import types
from utils.del_data_dirs import del_data_dirs
from utils.make_dirs import make_dirs
from utils.get_config import GetConfig
import polib

en_msgs = polib.pofile('locales/en/drop_data.po')


async def drop_data_rout(message: types.Message) -> None:
    creator_id: int = GetConfig.get_bot_config()["Settings"]["creator_id"]
    user_id: int = message.from_user.id

    if user_id != creator_id:
        await message.answer(en_msgs.find('unknown_command_msg'))

    else:
        try:
            await del_data_dirs()
            await make_dirs()
        except FileNotFoundError:
            pass
        finally:
            await message.answer(en_msgs.find('hope_msg'))

    return
