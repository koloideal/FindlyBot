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


async def swipe_items_callback(
    callback: CallbackQuery, callback_data: SwipeItemsCallbackData
):
    current_marketplace = callback_data.marketplace
    current_item_id = callback_data.current_item_id
    query = callback_data.query
    requester_id = callback.from_user.id
    hash_query = await req_to_hash(query.replace(" ", "+"))

    with open(
        f"local_data/products_data/{requester_id}/{hash_query}.json", "r"
    ) as response:
        api_json_data: dict = json.load(response)

    current_item_link = api_json_data[current_marketplace][current_item_id]["link"]
    current_item_image_link = api_json_data[current_marketplace][current_item_id][
        "image"
    ]
    current_item_price = api_json_data[current_marketplace][current_item_id]["price"]
    current_item_name = api_json_data[current_marketplace][current_item_id]["name"]
    current_item_hash_name = await req_to_hash(current_item_name)

    max_item_id = max([x["id"] for x in api_json_data[current_marketplace]])

    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    if 0 < current_item_id < max_item_id:
        builder.add(
            InlineKeyboardButton(
                text="<<",
                callback_data=SwipeItemsCallbackData(
                    marketplace=current_marketplace,
                    current_item_id=current_item_id - 1,
                    query=query,
                ).pack(),
            ),
        )
        builder.add(
            InlineKeyboardButton(
                text=">>",
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
                text=">>",
                callback_data=SwipeItemsCallbackData(
                    marketplace=current_marketplace, current_item_id=1, query=query
                ).pack(),
            ),
        )

    elif current_item_id == max_item_id:
        builder.add(
            InlineKeyboardButton(
                text="<<",
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
            f"local_data/images/{requester_id}/{hash_query}/{current_marketplace}/{current_item_hash_name}.jpg"
        )

    res_name = await reformat_name(current_item_name.replace("_", " "), query)

    await callback.message.edit_media(
        InputMediaPhoto(
            media=image,
            caption=f"<i>place</i>:  <b>{current_marketplace}</b>\n\n"
            f'<i>name</i>:  <b><a href="{current_item_link}">{res_name}</a></b>\n\n'
            f"<i>price</i>:  <b>{current_item_price}</b> BYN\n\n"
            f"<i>position</i>:  <b>{current_item_id}</b>",
        ),
        reply_markup=builder.as_markup(),
    )


async def callback_query_rout_for_only_new(callback: CallbackQuery):
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    match callback.data:
        case "is_only_new_OFF":
            await ActionsOnUsers.change_only_new_config(callback)

            builder.add(
                InlineKeyboardButton(
                    text="Change Max Size", callback_data="change_max_size"
                ),
                InlineKeyboardButton(
                    text="Only New:  ON ✅", callback_data="is_only_new_ON"
                ),
            )

            await callback.message.edit_reply_markup(reply_markup=builder.as_markup())

        case "is_only_new_ON":
            await ActionsOnUsers.change_only_new_config(callback)

            builder.add(
                InlineKeyboardButton(
                    text="Change Max Size", callback_data="change_max_size"
                ),
                InlineKeyboardButton(
                    text="Only New:  OFF ❌", callback_data="is_only_new_OFF"
                ),
            )

            await callback.message.edit_reply_markup(reply_markup=builder.as_markup())


async def change_max_size_callback(callback: CallbackQuery, state: FSMContext):
    text: str = escape("0 < max_size < 21")
    await callback.message.answer(
        f"Enter new max size products in every marketplace\n"
        f"Max size must be: <b><u>{text}</u></b>"
    )

    await state.set_state(WaitMaxSize.wait_max_size)
