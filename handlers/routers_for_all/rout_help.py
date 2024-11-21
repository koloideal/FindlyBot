from aiogram.types import Message
import polib
from database_func.actions_on_users import ActionsOnUsers

en_msgs = polib.pofile('locales/en/rout_help.po')
ru_msgs = polib.pofile('locales/ru/rout_help.po')


async def button_to_help_rout(message: Message) -> None:
    user_id = message.from_user.id
    lang: str = await ActionsOnUsers.get_user_lang_config(user_id=user_id)

    match lang:
        case "RU":
            msgs = ru_msgs
        case "EN":
            msgs = en_msgs
        case _:
            msgs = en_msgs
    await message.answer(
        msgs.find("help_rout_msg").msgstr,
        parse_mode="HTML",
        disable_web_page_preview=True
    )
