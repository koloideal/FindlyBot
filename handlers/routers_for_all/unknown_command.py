import polib
from aiogram import types
from database_func.users_dao import ActionsOnUsers

en_msgs = polib.pofile("locales/en/unknown_command.po")
ru_msgs = polib.pofile("locales/ru/unknown_command.po")


async def unknown_command(message: types.Message) -> None:
    user_id = message.from_user.id
    user_config: dict = await ActionsOnUsers.get_all_configs(user_id=user_id)
    lang: str = user_config["language"]
    match lang:
        case "RU":
            msgs = ru_msgs
        case "EN":
            msgs = en_msgs
        case _:
            msgs = en_msgs
    await message.answer(msgs.find("unknown_msg").msgstr)
