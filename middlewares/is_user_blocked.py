from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from database_func.database_models import UserConfig, BannedUser
from database_func.users_config_dao import UsersConfigDAO
from database_func.banned_users_dao import BannedUsersDAO
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
        banned_users: list[BannedUser] = BannedUsersDAO().get_banned_users()
        banned_users_ids: list[int] = [banned_user.user_id for banned_user in banned_users]
        user_id: int = event.from_user.id

        params: dict[str, int | str] = UserConfig.get_default_user_config(user_id=user_id)
        UsersConfigDAO().config_user_to_database(params=params)

        user_config: UserConfig = UsersConfigDAO().get_all_configs(user_id=user_id)
        language: str = user_config.language

        match language:
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