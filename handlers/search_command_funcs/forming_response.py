import re
from aiogram.types import Message, InlineKeyboardButton, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.query_to_hash import req_to_hash
from ..custom_callback_data.swipe_items_callback_data import SwipeItemsCallbackData
import json
from utils.reformat_name import reformat_name


async def forming_response(message: Message, query: str, wait_message: Message):
    query_without_plus: str = re.sub(r"\+", " ", query)
    requestor_id: int = message.from_user.id
    query_hash: str = await req_to_hash(query)

    with open(
        f"local_data/products_data/{requestor_id}/{query_hash}.json", "r"
    ) as response:
        api_json_data: dict = json.load(response)

    await wait_message.delete()

    for marketplace in api_json_data:
        item = api_json_data[marketplace][0]
        link = item["link"]
        image_link = item["image"]
        name = item["name"]
        name_hash = await req_to_hash(name)
        price = item["price"]
        ids = item["id"]

        res_name = await reformat_name(name.replace("_", " "), query_without_plus)

        if image_link == "images/placeholder.png":
            image = FSInputFile("local_data/images/placeholder.jpg")
        else:
            image = FSInputFile(
                f"local_data/images/{requestor_id}/{query_hash}/{marketplace}/{name_hash}.jpg"
            )

        if len(api_json_data[marketplace]) > 1:
            builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
            builder.add(
                InlineKeyboardButton(
                    text=">>",
                    callback_data=SwipeItemsCallbackData(
                        marketplace=marketplace,
                        current_item_id=int(ids) + 1,
                        query=query_without_plus,
                    ).pack(),
                ),
            )
            await message.answer_photo(
                image,
                caption=f"<i>place</i>:  <b>{marketplace}</b>\n\n"
                f'<i>name</i>:  <b><a href="{link}">{res_name}</a></b>\n\n'
                f"<i>price</i>:  <b>{price}</b> BYN\n\n"
                f"<i>position</i>:  <b>{ids}</b>",
                reply_markup=builder.as_markup(),
            )

        else:
            await message.answer_photo(
                image,
                caption=f"<i>place</i>:  <b>{marketplace}</b>\n\n"
                f'<i>name</i>:  <b><a href="{link}">{res_name}</a></b>\n\n'
                f"<i>price</i>:  <b>{price}</b> BYN",
            )
