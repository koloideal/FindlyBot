import polib
from aiogram import types

from database_func.database_models import UserConfig
from database_func.users_config_dao import UsersConfigDAO


en_msgs = polib.pofile("locales/en/unknown_command.po")
ru_msgs = polib.pofile("locales/ru/unknown_command.po")


async def unknown_command(message: types.Message) -> None:
    user_id = message.from_user.id
    user_config: UserConfig = UsersConfigDAO().get_all_configs(user_id=user_id)
    language: str = user_config.language
    match language:
        case "RU":
            msgs = ru_msgs
        case "EN":
            msgs = en_msgs
        case _:
            msgs = en_msgs
    await message.answer(msgs.find("unknown_msg").msgstr)
