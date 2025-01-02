from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from database_func.actions_on_users import ActionsOnUsers
import polib

en_msgs = polib.pofile("locales/en/is_user_blocked.po")
ru_msgs = polib.pofile("locales/ru/is_user_blocked.po")


class RejectBlockedUserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        banned_users_ids = await ActionsOnUsers.get_banned_users()
        user_id = event.from_user.id
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

        if user_id in banned_users_ids:
            await event.answer(
                msgs.find("banned_user_case_msg").msgstr,
                disable_web_page_preview=True,
            )
        else:
            return await handler(event, data)