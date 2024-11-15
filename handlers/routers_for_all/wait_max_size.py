from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from database_func.actions_on_users import ActionsOnUsers
from html import escape
import polib

en_msgs = polib.pofile('locales/en/wait_max_size.po')
ru_msgs = polib.pofile('locales/ru/wait_max_size.po')


async def get_max_size_rout(message: Message, state: FSMContext) -> None:
    try:
        max_size: int = int(message.text.strip())
        if not 0 < max_size < 21:
            raise ValueError
    except ValueError:
        text: str = escape("0 < max_size < 21")
        await message.answer(en_msgs.find('incorrect_value_msg').format(text=text))
    else:
        await ActionsOnUsers.change_max_size_config(message)
        await message.answer(en_msgs.find('change_max_size_msg').format(max_size=max_size))
        await state.clear()
