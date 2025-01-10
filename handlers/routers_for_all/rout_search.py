from aiogram.types import Message
from database_func.database_models import UserConfig
from database_func.users_config_dao import UsersConfigDAO
from aiogram.fsm.context import FSMContext
from states.user_states import WaitQuery
from utils.check_responses import check_responses
import polib

en_msgs = polib.pofile("locales/en/rout_search.po")
ru_msgs = polib.pofile("locales/ru/rout_search.po")


async def search_rout(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    user_config: UserConfig = UsersConfigDAO().get_all_configs(user_id=user_id)
    language: str = user_config.language

    match language:
        case "RU":
            msgs = ru_msgs
        case "EN":
            msgs = en_msgs
        case _:
            msgs = en_msgs

    is_full_responses = await check_responses(user_id)
    if is_full_responses:
        await message.answer(msgs.find("full_responses_msg").msgstr)
    await message.answer(msgs.find("enter_query_msg").msgstr)
    await state.set_state(WaitQuery.wait_query)
