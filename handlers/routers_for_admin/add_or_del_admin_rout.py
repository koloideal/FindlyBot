from aiogram import types
from states.admin_states import AdminState
from aiogram.fsm.context import FSMContext
from utils.get_config import GetConfig


async def add_or_del_admin_rout(
    message: types.Message, del_or_add: str, state: FSMContext
) -> None:
    creator_id: int = GetConfig.get_bot_config()["Settings"]["creator_id"]
    user_id: int = message.from_user.id

    if user_id != creator_id:
        await message.answer("Unknown command, enter /help")

    else:
        await message.answer("Enter a username")

        match del_or_add:
            case "add":
                await state.set_state(AdminState.waiting_for_add_admin)
            case "del":
                await state.set_state(AdminState.waiting_for_del_admin)
    return
