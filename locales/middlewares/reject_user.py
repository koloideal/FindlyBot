from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message

from database.dao.admins_dao import AdminsDAO
from database.dao.banned_users_dao import BannedUsersDAO
from database.database_models import UserConfig, BannedUser, Admin
from database.dao.users_config_dao import UsersConfigDAO
import polib
from utils.get_config import GetConfig


config: dict = GetConfig.get_bot_config()
en_msgs = polib.pofile("locales/en/reject_user.po")
ru_msgs = polib.pofile("locales/ru/reject_user.po")
creator_id: str = config["Settings"]["creator_id"]


class RejectUserMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]) -> Any:
        user_id: str = str(event.from_user.id)
        input_command = event.text.strip()

        params: tuple = UserConfig.get_default_user_config(user_id=user_id)
        UsersConfigDAO().config_user_to_database(params=params)
        user_config: UserConfig = UsersConfigDAO().get_all_configs(user_id=user_id)
        language: str =  user_config.language

        banned_users: list[BannedUser] = BannedUsersDAO().get_banned_users()
        banned_users_ids: list[str] = [banned_user.user_id for banned_user in banned_users]

        admins: list[Admin] = AdminsDAO().get_admins()
        admin_ids: list[str] = [x.user_id for x in admins]

        match language:
            case "RU":
                msgs = ru_msgs
            case "EN":
                msgs = en_msgs
            case _:
                msgs = en_msgs

        creator_commands = ['/add_admin', '/del_admin', 'drop_data', '/get_admins']
        admin_commands = ['/ban_user', '/unban_user', '/get_main_logs', '/get_action_logs']

        if user_id in banned_users_ids and user_id != creator_id:
            await event.answer(msgs.find("banned_user_case_msg").msgstr,
                               disable_web_page_preview=True)
            return

        if input_command in creator_commands:
            if user_id == creator_id:
                return await handler(event, data)
            else:
                await event.answer(msgs.find("unknown_command_msg").msgstr)
        elif input_command in admin_commands:
            if user_id in admin_ids or user_id == creator_id:
                return await handler(event, data)
            else:
                await event.answer(msgs.find("unknown_command_msg").msgstr)
        else:
            return await handler(event, data)