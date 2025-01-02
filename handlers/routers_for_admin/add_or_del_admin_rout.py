from aiogram import types
from states.admin_states import AdminState
from aiogram.fsm.context import FSMContext
from database_func.actions_on_users import ActionsOnUsers
import polib
from polib import POFile


en_msgs: POFile = polib.pofile("locales/en/add_or_del_admin_rout.po")
ru_msgs: POFile = polib.pofile("locales/ru/add_or_del_admin_rout.po")


async def add_or_del_admin_rout(
    message: types.Message, del_or_add: str, state: FSMContext
) -> None:
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
    await message.answer(msgs.find("enter_username_msg").msgstr)
    match del_or_add:
        case "add":
            await state.set_state(AdminState.waiting_for_add_admin)
        case "del":
            await state.set_state(AdminState.waiting_for_del_admin)
