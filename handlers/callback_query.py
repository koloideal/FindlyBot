import json
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    InputMediaPhoto,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from states.user_states import WaitMaxSize
from database_func.actions_on_users import ActionsOnUsers
from utils.query_to_hash import req_to_hash
from utils.reformat_name import reformat_name
from .custom_callback_data.swipe_items_callback_data import SwipeItemsCallbackData
from html import escape
import polib


en_msgs = polib.pofile('locales/en/callback_query.po')
ru_msgs = polib.pofile('locales/ru/callback_query.po')


async def swipe_items_callback(callback: CallbackQuery,
                               callback_data: SwipeItemsCallbackData):
    current_marketplace = callback_data.marketplace
    current_item_id = callback_data.current_item_id
    query = callback_data.query
    requestor_id = callback.from_user.id
    hash_query = await req_to_hash(query.replace(" ", "+"))

    lang: str = await ActionsOnUsers.get_user_lang_config(user_id=requestor_id)

    match lang:
        case "RU":
            msgs = ru_msgs
        case "EN":
            msgs = en_msgs
        case _:
            msgs = en_msgs

    with open(
        f"local_data/products_data/{requestor_id}/{hash_query}.json", "r"
    ) as response:
        api_json_data: dict = json.load(response)

    current_item_link = api_json_data[current_marketplace][current_item_id]["link"]
    current_item_image_link = api_json_data[current_marketplace][current_item_id]["image"]
    current_item_price = api_json_data[current_marketplace][current_item_id]["price"]
    current_item_name = api_json_data[current_marketplace][current_item_id]["name"]
    current_item_hash_name = await req_to_hash(current_item_name)
    size_of_products = len(api_json_data[current_marketplace])

    max_item_id = max([x["id"] for x in api_json_data[current_marketplace]])

    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    if 0 < current_item_id < max_item_id:
        builder.add(
            InlineKeyboardButton(
                text="⬅",
                callback_data=SwipeItemsCallbackData(
                    marketplace=current_marketplace,
                    current_item_id=current_item_id - 1,
                    query=query,
                ).pack(),
            ),
        )
        builder.add(
            InlineKeyboardButton(
                text="➡",
                callback_data=SwipeItemsCallbackData(
                    marketplace=current_marketplace,
                    current_item_id=current_item_id + 1,
                    query=query,
                ).pack(),
            ),
        )

    elif current_item_id == 0:
        builder.add(
            InlineKeyboardButton(
                text="➡",
                callback_data=SwipeItemsCallbackData(
                    marketplace=current_marketplace, current_item_id=1, query=query
                ).pack(),
            ),
        )

    elif current_item_id == max_item_id:
        builder.add(
            InlineKeyboardButton(
                text="⬅",
                callback_data=SwipeItemsCallbackData(
                    marketplace=current_marketplace,
                    current_item_id=max_item_id - 1,
                    query=query,
                ).pack(),
            ),
        )

    if current_item_image_link == "images/placeholder.png":
        image = FSInputFile("local_data/images/placeholder.jpg")
    else:
        image = FSInputFile(
            f"local_data/images/{requestor_id}/{hash_query}/{current_marketplace}/{current_item_hash_name}.jpg"
        )

    res_name = await reformat_name(current_item_name.replace("_", " "), query)

    await callback.message.edit_media(
        InputMediaPhoto(
            media=image,
            caption=msgs.find('many_cards_msg').msgstr
                                                  .format(current_marketplace=current_marketplace,
                                                          current_item_link=current_item_link,
                                                          res_name=res_name,
                                                          current_item_price=current_item_price,
                                                          current_item_id=current_item_id,
                                                          size_of_products=size_of_products),
        ),
        reply_markup=builder.as_markup(),
    )


async def callback_query_rout_for_only_new(callback: CallbackQuery):
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    user_id = int(callback.from_user.id)
    lang: str = await ActionsOnUsers.get_user_lang_config(user_id=user_id)

    match lang:
        case "RU":
            msgs = ru_msgs
        case "EN":
            msgs = en_msgs
        case _:
            msgs = en_msgs

    match callback.data:
        case "is_only_new_OFF":
            callback_data = callback.data
            await ActionsOnUsers.change_only_new_config(callback_data=callback_data,
                                                        user_id=user_id)

            builder.add(
                InlineKeyboardButton(
                    text=msgs.find('ch_max_size_msg').msgstr, callback_data="change_max_size"
                ),
                InlineKeyboardButton(
                    text=msgs.find('only_new_on_msg').msgstr, callback_data="is_only_new_ON"
                ),
            )

            await callback.message.edit_reply_markup(reply_markup=builder.as_markup())

        case "is_only_new_ON":
            callback_data = callback.data
            await ActionsOnUsers.change_only_new_config(callback_data=callback_data,
                                                        user_id=user_id)

            builder.add(
                InlineKeyboardButton(
                    text=msgs.find('ch_max_size_msg').msgstr, callback_data="change_max_size"
                ),
                InlineKeyboardButton(
                    text=msgs.find('only_new_off_msg').msgstr, callback_data="is_only_new_OFF"
                ),
            )

            await callback.message.edit_reply_markup(reply_markup=builder.as_markup())


async def change_max_size_callback(callback: CallbackQuery, state: FSMContext):
    text: str = escape("0 < max_size < 21")
    user_id = int(callback.from_user.id)
    lang: str = await ActionsOnUsers.get_user_lang_config(user_id=user_id)
    match lang:
        case "RU":
            msgs = ru_msgs
        case "EN":
            msgs = en_msgs
        case _:
            msgs = en_msgs
    await callback.message.answer(msgs.find('max_size_msg').msgstr.format(text=text))

    await state.set_state(WaitMaxSize.wait_max_size)
