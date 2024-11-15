from aiogram import types
from states.admin_states import AdminState
from aiogram.fsm.context import FSMContext
from database_func.action_on_admin import ActionsOnAdmin
from utils.get_config import GetConfig
import polib


en_msgs = polib.pofile('locales/en/ban_or_unban_rout.po')


async def ban_or_unban_user_rout(
    message: types.Message, ban_or_unban: str, state: FSMContext
) -> None:
    creator_id: int = GetConfig.get_bot_config()["Settings"]["creator_id"]
    user_id: int = message.from_user.id

    admins_id: list = await ActionsOnAdmin.get_admins()

    if user_id != creator_id and user_id not in admins_id:
        await message.answer(en_msgs.find('unknown_command_msg'))

    else:
        await message.answer(en_msgs.find('enter_username_msg'))

        match ban_or_unban:
            case "ban":
                await state.set_state(AdminState.waiting_for_ban_user)
            case "unban":
                await state.set_state(AdminState.waiting_for_unban_user)
    return
