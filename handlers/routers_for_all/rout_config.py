import polib
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database_func.actions_on_users import ActionsOnUsers

en_msgs = polib.pofile('locales/en/rout_config.po')
ru_msgs = polib.pofile('locales/ru/rout_config.po')


async def config_rout(message: types.Message) -> None:
    user_id = message.from_user.id
    lang: str = await ActionsOnUsers.get_user_lang_config(user_id=user_id)

    match lang:
        case "RU":
            msgs = ru_msgs
        case "EN":
            msgs = en_msgs
        case _:
            msgs = en_msgs

    lang_msg = msgs.find("lang_ru_msg").msgstr if lang == 'RU' else msgs.find("lang_en_msg").msgstr
    lang_callback_data = 'lang_EN' if lang == 'RU' else 'lang_RU'

    is_only_new: bool = await ActionsOnUsers.get_user_only_new_config(user_id)
    is_only_new_msg = msgs.find("only_new_on_msg").msgstr if is_only_new else msgs.find("only_new_off_msg").msgstr
    is_only_new_callback_data = "is_only_new_ON" if is_only_new else "is_only_new_OFF"

    max_size: int = await ActionsOnUsers.get_user_max_size_config(user_id)

    buttons: list = [
        [
            InlineKeyboardButton(text=is_only_new_msg, callback_data=is_only_new_callback_data),
            InlineKeyboardButton(text=lang_msg, callback_data=lang_callback_data)
        ],
        [
            InlineKeyboardButton(text=msgs.find("ch_max_size_msg").msgstr, callback_data="change_max_size")
        ]
    ]

    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=buttons)

    await message.answer(
        msgs.find("config_rout_msg").msgstr.format(max_size=max_size),
        reply_markup=keyboard,
    )
