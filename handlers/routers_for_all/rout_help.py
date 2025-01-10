from aiogram.types import Message
import polib
from database_func.database_models import UserConfig
from database_func.users_config_dao import UsersConfigDAO

en_msgs = polib.pofile("locales/en/rout_help.po")
ru_msgs = polib.pofile("locales/ru/rout_help.po")


async def button_to_help_rout(message: Message) -> None:
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
    await message.answer(
        msgs.find("help_rout_msg").msgstr,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )
