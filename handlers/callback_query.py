import json
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    InputMediaPhoto,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
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

    user_config: dict = await ActionsOnUsers.get_all_configs(user_id=requestor_id)
    lang: str = user_config['language']

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
                                                          current_item_id=current_item_id+1,
                                                          size_of_products=size_of_products),
        ),
        reply_markup=builder.as_markup(),
    )


async def callback_query_change_only_new(callback: CallbackQuery):
    callback_data = callback.data
    user_id = int(callback.from_user.id)
    user_config: dict = await ActionsOnUsers.get_all_configs(user_id=user_id)
    lang: str = user_config['language']

    await ActionsOnUsers.change_only_new_config(callback_data=callback_data,
                                                user_id=user_id)

    match lang:
        case "RU":
            msgs = ru_msgs
        case "EN":
            msgs = en_msgs
        case _:
            msgs = en_msgs

    lang_msg = msgs.find("lang_ru_msg").msgstr if lang == 'RU' else msgs.find("lang_en_msg").msgstr
    lang_callback_data = 'lang_EN' if lang == 'RU' else 'lang_RU'

    is_only_new_msg = msgs.find("only_new_on_msg").msgstr if callback_data == 'is_only_new_OFF' else msgs.find("only_new_off_msg").msgstr
    is_only_new_callback_data = "is_only_new_ON" if callback_data == 'is_only_new_OFF' else "is_only_new_OFF"

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

    await callback.message.edit_reply_markup(reply_markup=keyboard)


async def callback_query_change_lang(callback: CallbackQuery):
    callback_data = callback.data
    user_id = int(callback.from_user.id)
    await ActionsOnUsers.change_lang_config(callback_data=callback_data,
                                            user_id=user_id)
    user_config: dict = await ActionsOnUsers.get_all_configs(user_id=user_id)
    lang: str = user_config['language']
    max_size: int = user_config['max_size']

    match lang:
        case "RU":
            msgs = ru_msgs
        case "EN":
            msgs = en_msgs
        case _:
            msgs = en_msgs

    lang_msg = msgs.find("lang_ru_msg").msgstr if lang == 'RU' else msgs.find("lang_en_msg").msgstr
    lang_callback_data = 'lang_RU' if callback_data == 'lang_EN' else 'lang_EN'

    is_only_new: bool = await ActionsOnUsers.get_user_only_new_config(user_id)
    is_only_new_msg = msgs.find("only_new_on_msg").msgstr if is_only_new else msgs.find("only_new_off_msg").msgstr
    is_only_new_callback_data = "is_only_new_ON" if is_only_new else "is_only_new_OFF"

    text = msgs.find("edit_lang_msg").msgstr.format(max_size=max_size)
    
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
    await callback.message.edit_text(text=text,reply_markup=keyboard)


async def change_max_size_callback(callback: CallbackQuery, state: FSMContext):
    text: str = escape("0 < max_size < 21")
    user_id = int(callback.from_user.id)
    user_config: dict = await ActionsOnUsers.get_all_configs(user_id=user_id)
    lang: str = user_config['language']

    match lang:
        case "RU":
            msgs = ru_msgs
        case "EN":
            msgs = en_msgs
        case _:
            msgs = en_msgs
    await callback.message.answer(msgs.find('max_size_msg').msgstr.format(text=text))

    await state.set_state(WaitMaxSize.wait_max_size)
