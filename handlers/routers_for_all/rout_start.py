from aiogram.types import Message
from database_func.actions_on_users import ActionsOnUsers
from database_func.action_on_admin import ActionsOnAdmin
from utils.get_config import GetConfig
import polib

data = polib.pofile('locales/en/rout_start.po')


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
            data.find("creator_case_msg")
        )

    elif admin_case:
        await message.answer(
            data.find("admin_case_msg"),
            disable_web_page_preview=True,
        )

    elif user_case:
        await message.answer(
            data.find("user_case_msg"),
            disable_web_page_preview=True,
        )

    elif banned_user_case:
        await message.answer(
            data.find("banned_user_case_msg"),
            disable_web_page_preview=True,
        )

    username = message.from_user.username
    first_name = message.from_user.first_name

    await ActionsOnUsers.user_to_database(user_id=user_id,
                                          first_name=first_name,
                                          username=username)
