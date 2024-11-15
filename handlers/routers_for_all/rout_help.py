from aiogram.types import Message
import polib

en_msgs = polib.pofile('locales/en/rout_help.po')
ru_msgs = polib.pofile('locales/ru/rout_help.po')


async def button_to_help_rout(message: Message) -> None:
    await message.answer(
        en_msgs.find("help_rout_msg"),
        parse_mode="HTML",
        disable_web_page_preview=True
    )
