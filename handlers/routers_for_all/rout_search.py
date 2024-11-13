from aiogram.types import Message
from database_func.actions_on_users import ActionsOnUsers
from aiogram.fsm.context import FSMContext
from states.user_states import WaitQuery
from utils.check_responses import check_responses


async def search_rout(message: Message, state: FSMContext) -> None:
    banned_users_ids: list = await ActionsOnUsers.get_banned_users()

    if message.from_user.id in banned_users_ids:
        await message.answer(
            "Hello, I am a <b>Findly</b>🤖\n\n"
            "Fast and smart search engine for the best products on marketplaces 💭"
            "\n\n<u><b>You were blocked</b></u>"
            "\n\n\nAbout the unban - <a href='https://t.me/kolo_id'>kolo</a>",
            disable_web_page_preview=True,
        )
    else:
        await ActionsOnUsers.config_user_to_database(message)
        is_full_responses = await check_responses(message.from_user.id)
        if is_full_responses:
            await message.answer(
                "You have reached the limit of saved responses, "
                "the oldest response has been deleted"
            )
        await message.answer("Enter query for searching")
        await state.set_state(WaitQuery.wait_query)
