from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from database_func.actions_on_users import ActionsOnUsers
import polib
from utils.get_config import GetConfig


config: dict = GetConfig.get_bot_config()
en_msgs = polib.pofile("locales/en/is_user_creator.po")
ru_msgs = polib.pofile("locales/ru/is_user_creator.po")
creator_id: int = config["Settings"]["creator_id"]


class RejectNotCreatorMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
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
        creator_commands = ['/add_admin', '/del_admin', 'drop_data', '/get_admins']
        if event.text.strip() in creator_commands:
            if user_id == creator_id:
                return await handler(event, data)
            else:
                await event.answer(msgs.find("unknown_command_msg").msgstr)
        else:
            return await handler(event, data)