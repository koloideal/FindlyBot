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

    if user_id in banned_users_ids:
        await message.answer(
            en_msgs.find('banned_rout_search_msg'),
            disable_web_page_preview=True,
        )
    else:
        await ActionsOnUsers.config_user_to_database(message)
        is_full_responses = await check_responses(user_id)
        if is_full_responses:
            await message.answer(en_msgs.find('full_responses_msg'))
        await message.answer(en_msgs.find('enter_query_msg'))
        await state.set_state(WaitQuery.wait_query)
