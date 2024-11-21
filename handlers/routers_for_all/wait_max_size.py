from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from database_func.actions_on_users import ActionsOnUsers
from html import escape
import polib

en_msgs = polib.pofile('locales/en/wait_max_size.po')
ru_msgs = polib.pofile('locales/ru/wait_max_size.po')


async def get_max_size_rout(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    lang: str = await ActionsOnUsers.get_user_lang_config(user_id=user_id)

    match lang:
        case "RU":
            msgs = ru_msgs
        case "EN":
            msgs = en_msgs
        case _:
            msgs = en_msgs
    try:
        max_size: int = int(message.text.strip())
        if not 0 < max_size < 21:
            raise ValueError
    except ValueError:
        text: str = escape("0 < max_size < 21")
        await message.answer(msgs.find('incorrect_value_msg').msgstr.format(text=text))
    else:
        user_id = message.from_user.id
        await ActionsOnUsers.change_max_size_config(user_id=user_id,
                                                    max_size=max_size)
        await message.answer(msgs.find('change_max_size_msg').msgstr.format(max_size=max_size))
        await state.clear()
