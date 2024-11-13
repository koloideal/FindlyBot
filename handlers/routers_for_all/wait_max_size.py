from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from database_func.actions_on_users import ActionsOnUsers
from html import escape


async def get_max_size_rout(message: Message, state: FSMContext) -> None:
    try:
        max_size: int = int(message.text.strip())
        if not 0 < max_size < 21:
            raise ValueError
    except ValueError:
        text: str = escape("0 < max_size < 21")
        await message.answer(
            "Incorrect value\n" f"Max size must be: <b><u>{text}</u></b>"
        )
    else:
        await ActionsOnUsers.change_max_size_config(message)
        await message.answer(
            f"Max size has been changed, now: <b><u>{max_size}</u></b>"
        )
        await state.clear()
