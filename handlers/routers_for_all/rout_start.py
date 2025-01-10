from aiogram.types import Message
from database_func.users_dao import ActionsOnUsers
from database_func.admins_dao import ActionsOnAdmin
from utils.get_config import GetConfig
import polib

en_msgs = polib.pofile("locales/en/rout_start.po")
ru_msgs = polib.pofile("locales/ru/rout_start.po")


async def start_rout(message: Message) -> None:

    user_id: int = message.from_user.id
    admins_ids: list = await ActionsOnAdmin.get_admins(only_ids=True)
    creator_id: int = int(GetConfig.get_bot_config()["Settings"]["creator_id"])

    await ActionsOnUsers.config_user_to_database(user_id)
    user_config: dict = await ActionsOnUsers.get_all_configs(user_id=user_id)
    lang: str = user_config["language"]

    match lang:
        case "RU":
            msgs = ru_msgs
        case "EN":
            msgs = en_msgs
        case _:
            msgs = en_msgs

    case1: bool = user_id in admins_ids and user_id == creator_id
    case2: bool = user_id not in admins_ids and user_id == creator_id
    case3: bool = user_id in admins_ids and user_id != creator_id
    case4: bool = user_id not in admins_ids and user_id != creator_id

    creator_case: bool = case1 or case2
    admin_case: bool = case3 and not (case1 or case2)
    user_case: bool = case4

    if creator_case:
        await message.answer(msgs.find("creator_case_msg").msgstr)

    elif admin_case:
        await message.answer(
            msgs.find("admin_case_msg").msgstr,
            disable_web_page_preview=True,
        )

    elif user_case:
        await message.answer(
            msgs.find("user_case_msg").msgstr,
            disable_web_page_preview=True,
        )

    username = message.from_user.username
    first_name = message.from_user.first_name

    await ActionsOnUsers.user_to_database(
        user_id=user_id, first_name=first_name, username=username
    )
