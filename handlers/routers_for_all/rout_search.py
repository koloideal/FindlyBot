from aiogram.types import Message
from database_func.actions_on_users import ActionsOnUsers
from aiogram.fsm.context import FSMContext
from states.user_states import WaitQuery
from utils.check_responses import check_responses
import polib

en_msgs = polib.pofile('locales/en/rout_search.po')
ru_msgs = polib.pofile('locales/ru/rout_search.po')


async def search_rout(message: Message, state: FSMContext) -> None:
    banned_users_ids: list = await ActionsOnUsers.get_banned_users()
    user_id = message.from_user.id

    user_config: dict = await ActionsOnUsers.get_all_configs(user_id=user_id)
    lang: str = user_config['language']

    match lang:
        case "RU":
            msgs = ru_msgs
        case "EN":
            msgs = en_msgs
        case _:
            msgs = en_msgs

    if user_id in banned_users_ids:
        await message.answer(
            msgs.find('banned_rout_search_msg').msgstr,
            disable_web_page_preview=True,
        )
    else:
        await ActionsOnUsers.config_user_to_database(user_id)
        is_full_responses = await check_responses(user_id)
        if is_full_responses:
            await message.answer(msgs.find('full_responses_msg').msgstr)
        await message.answer(msgs.find('enter_query_msg').msgstr)
        await state.set_state(WaitQuery.wait_query)
