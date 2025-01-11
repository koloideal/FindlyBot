from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from database.dao.admins_dao import AdminsDAO
from database.database_models import Admin, UserConfig
from database.dao.users_config_dao import UsersConfigDAO
import polib
from utils.get_config import GetConfig


config: dict = GetConfig.get_bot_config()
en_msgs = polib.pofile("locales/en/is_user_admin.po")
ru_msgs = polib.pofile("locales/ru/is_user_admin.po")
creator_id: int = config["Settings"]["creator_id"]


class RejectNotAdminMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        admin_ids: list[Admin] = AdminsDAO().get_admins()
        admin_ids: list[int] = [x.user_id for x in admin_ids]
        user_id = event.from_user.id

        params: tuple = UserConfig.get_default_user_config(user_id=user_id)
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
        admin_commands = ['/ban_user', '/unban_user', '/get_main_logs', '/get_action_logs']
        if event.text.strip() in admin_commands:
            if user_id in admin_ids or user_id == creator_id:
                return await handler(event, data)
            else:
                await event.answer(msgs.find("unknown_command_msg").msgstr)
        else:
            return await handler(event, data)