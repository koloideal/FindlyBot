import re
from aiogram.types import Message, InlineKeyboardButton, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.query_to_hash import req_to_hash
from ..custom_callback_data.swipe_items_callback_data import SwipeItemsCallbackData
import json
from utils.reformat_name import reformat_name
import polib


en_msgs = polib.pofile('locales/en/forming_response.po')
ru_msgs = polib.pofile('locales/ru/forming_response.po')


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

        size_of_products = len(api_json_data[marketplace])

        if size_of_products > 1:
            builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
            builder.add(
                InlineKeyboardButton(
                    text="➡",
                    callback_data=SwipeItemsCallbackData(
                        marketplace=marketplace,
                        current_item_id=int(ids) + 1,
                        query=query_without_plus,
                    ).pack(),
                ),
            )
            await message.answer_photo(
                image,
                caption=en_msgs.find('many_cards_msg').msgstr
                                                      .format(marketplace=marketplace,
                                                              link=link,
                                                              res_name=res_name,
                                                              price=price,
                                                              ids=ids,
                                                              size_of_products=size_of_products),
                reply_markup=builder.as_markup(),
            )

        else:
            await message.answer_photo(
                image,
                caption=en_msgs.find('one_card_msg').msgstr
                                                    .format(marketplace=marketplace,
                                                            link=link,
                                                            res_name=res_name,
                                                            price=price,
                                                            ids=ids),
            )
