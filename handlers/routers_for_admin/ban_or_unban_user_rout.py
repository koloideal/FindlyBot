from aiogram import types
from database_func.actions_on_users import ActionsOnUsers
from states.admin_states import AdminState
from aiogram.fsm.context import FSMContext
from database_func.action_on_admin import ActionsOnAdmin
from utils.get_config import GetConfig
import polib
from polib import POFile


en_msgs: POFile = polib.pofile("locales/en/ban_or_unban_user_rout.po")
ru_msgs: POFile = polib.pofile("locales/ru/ban_or_unban_user_rout.po")


async def ban_or_unban_user_rout(
    message: types.Message, ban_or_unban: str, state: FSMContext
) -> None:
    creator_id: int = GetConfig.get_bot_config()["Settings"]["creator_id"]
    user_id: int = message.from_user.id
    user_config: dict = await ActionsOnUsers.get_all_configs(user_id=user_id)
    lang: str = user_config["language"]

    match lang:
        case "RU":
            msgs: POFile = ru_msgs
        case "EN":
            msgs: POFile = en_msgs
        case _:
            msgs: POFile = en_msgs

    admins_id: list[int] = await ActionsOnAdmin.get_admins()

    if (user_id != creator_id) and (user_id not in admins_id):
        await message.answer(msgs.find("unknown_command_msg").msgstr)

    else:
        await message.answer(msgs.find("enter_username_msg").msgstr)

        match ban_or_unban:
            case "ban":
                await state.set_state(AdminState.waiting_for_ban_user)
            case "unban":
                await state.set_state(AdminState.waiting_for_unban_user)
