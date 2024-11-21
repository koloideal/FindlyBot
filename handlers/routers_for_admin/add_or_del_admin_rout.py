from aiogram import types
from states.admin_states import AdminState
from aiogram.fsm.context import FSMContext
from utils.get_config import GetConfig
from database_func.actions_on_users import ActionsOnUsers
import polib


en_msgs = polib.pofile('locales/en/add_or_del_admin_rout.po')
ru_msgs = polib.pofile('locales/ru/add_or_del_admin_rout.po')


async def add_or_del_admin_rout(message: types.Message,
                                del_or_add: str,
                                state: FSMContext) -> None:
    creator_id: int = GetConfig.get_bot_config()["Settings"]["creator_id"]
    user_id: int = message.from_user.id
    lang: str = await ActionsOnUsers.get_user_lang_config(user_id=user_id)

    match lang:
        case "RU":
            msgs = ru_msgs
        case "EN":
            msgs = en_msgs
        case _:
            msgs = en_msgs

    if user_id != creator_id:
        await message.answer(msgs.find('unknown_command_msg').msgstr)

    else:
        await message.answer(msgs.find('enter_username_msg').msgstr)

        match del_or_add:
            case "add":
                await state.set_state(AdminState.waiting_for_add_admin)
            case "del":
                await state.set_state(AdminState.waiting_for_del_admin)
    return
