from aiogram.types import Message


async def button_to_help_rout(message: Message) -> None:
    await message.answer(
        "This bot is a wrapper over the <b>Findly API</b>\n"
        "The main functionality is to provide the most relevant product results from such marketplaces as <i>Onliner, Kufar, MMG</i> and <i>21vek</i>\n"
        "For best results, use the most <b><u>accurate name of the product</u></b> you want to receive, "
        "as well as use different variations of the name, for example: <u>'samsung s24' and 'samsung galaxy s24'</u>\n\n"
        "<i>made by <a href='t.me/kolo_id'>kolo</a></i>",
        parse_mode="HTML",
    )
