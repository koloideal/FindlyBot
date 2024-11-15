from aiogram import types
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database_func.actions_on_users import ActionsOnUsers
import polib

en_msgs = polib.pofile('locales/en/rout_config.po')
ru_msgs = polib.pofile('locales/en/rout_config.po')


async def config_rout(message: types.Message) -> None:
    await ActionsOnUsers.config_user_to_database(message)

    is_only_new: bool = await ActionsOnUsers.get_user_only_new_config(
        message.from_user.id
    )
    max_size: int = await ActionsOnUsers.get_user_max_size_config(message.from_user.id)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    if is_only_new:
        builder.add(
            InlineKeyboardButton(
                text="Change Max Size", callback_data="change_max_size"
            ),
            InlineKeyboardButton(
                text="Only New:  ON ✅", callback_data="is_only_new_ON"
            ),
        )

    else:
        builder.add(
            InlineKeyboardButton(
                text="Change Max Size", callback_data="change_max_size"
            ),
            InlineKeyboardButton(
                text="Only New:  OFF ❌", callback_data="is_only_new_OFF"
            ),
        )

    await message.answer(
        en_msgs.find("config_rout_msg").format(max_size=max_size),
        reply_markup=builder.as_markup(),
    )
