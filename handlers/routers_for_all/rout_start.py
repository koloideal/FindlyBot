from aiogram.types import Message
from database_func.actions_on_users import ActionsOnUsers
from database_func.action_on_admin import ActionsOnAdmin
from utils.get_config import GetConfig


async def start_rout(message: Message) -> None:
    creator_id: int = int(GetConfig.get_bot_config()["Settings"]["creator_id"])

    user_id: int = message.from_user.id
    admins_id: list = await ActionsOnAdmin.get_admins()
    banned_users_id: list = await ActionsOnUsers.get_banned_users()

    case1: bool = user_id in admins_id and user_id == creator_id
    case2: bool = user_id not in admins_id and user_id == creator_id
    case3: bool = user_id in admins_id and user_id != creator_id
    case4: bool = user_id in banned_users_id
    case5: bool = user_id not in banned_users_id

    creator_case: bool = ((case1 and case5) or (case2 and case5)) and not case4
    admin_case: bool = case3 and case5 and not (case4 or case1 or case2)
    user_case: bool = case5 and not (case1 or case2 or case3 or case4)
    banned_user_case: bool = (case4 and not (case1 or case2 or case3 or case5)) or (
        case4 and case3
    )

    if creator_case:
        await message.answer(
            "Hello, <b>Creator</b>\n\n"
            "What do you want to do today? 💭"
            "\n\nFor reference click <b><i>/help</i></b> 👈\n\n"
            "To start searching click <b><i>/search</i></b>👈\n\n"
            "To config searching click <b><i>/config</i></b>👈\n\n"
            "---- Creator's Commands👇 ----\n\n"
            "Add admin - <b><i>/add_admin</i></b> 👈\n\n"
            "Delete admin - <b><i>/del_admin</i></b> 👈\n\n"
            "Ban the user - <b><i>/ban_user</i></b> 👈\n\n"
            "Unban the user - <b><i>/unban_user</i></b> 👈\n\n"
            "Get admins - <b><i>/get_admins</i></b> 👈\n\n"
            "Get logs - <b><i>/get_logs</i></b> 👈\n\n"
            "<strike>You know the rest</strike>"
            "\n\n\n<b><i>made by you 🫵</i></b>"
        )

    elif admin_case:
        await message.answer(
            "Hello, <b>admin</b>\n\n"
            "What do you want to do today? 💭"
            "\n\nFor reference, click <b><i>/help</i></b> 👈\n\n"
            "To start searching click <b><i>/search</i></b>👈\n\n"
            "To config searching click <b><i>/config</i></b>👈\n\n"
            "---- Admin Commands👇- ---\n\n"
            "Ban the user - <b><i>/ban_user</i></b> 👈\n\n"
            "Unban the user - <b><i>/unban_user</i></b> 👈"
            "Get logs - <b><i>/get_logs</i></b> 👈"
            "\n\n\n<b><i>made by <a href='https://t.me/kolo_id '>kolo</a></i></b>",
            disable_web_page_preview=True,
        )

    elif user_case:
        await message.answer(
            "Hello, I am a <b>Findly</b>🤖\n\n"
            "Fast and smart search engine for the best products on marketplaces 💭"
            "\n\nFor reference, click <b><i>/help</i></b> 👈\n\n"
            "To config searching click <b><i>/config</i></b>👈\n\n"
            "To start searching click <b><i>/search</i></b>👈"
            "\n\n\n<b><i>made by <a href='https://t.me/kolo_id'>kolo</a></i></b>",
            disable_web_page_preview=True,
        )

    elif banned_user_case:
        await message.answer(
            "Hello, I am a <b>Findly</b>🤖\n\n"
            "Fast and smart search engine for the best products on marketplaces 💭"
            "\n\n<u><b>You were blocked</b></u>"
            "\n\n\nAbout the unban to <a href='https://t.me/kolo_id'>kolo</a>",
            disable_web_page_preview=True,
        )

    await ActionsOnUsers.user_to_database(message)
