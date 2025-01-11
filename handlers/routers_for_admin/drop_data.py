from logging import Logger
from aiogram.types import Message
from polib import POFile, pofile

from database.database_models import UserConfig
from database.dao.users_config_dao import UsersConfigDAO
from utils.del_data_dirs import del_data_dirs
from utils.make_dirs import make_dirs
from utils.create_loggers import create_action_logger, create_main_logger


en_msgs: POFile = pofile("locales/en/drop_data.po")
ru_msgs: POFile = pofile("locales/ru/drop_data.po")


async def drop_data_rout(message: Message) -> None:
    user_id: int = message.from_user.id
    user_config: UserConfig = UsersConfigDAO().get_all_configs(user_id=user_id)
    language: str = user_config.language

    match language:
        case "RU":
            msgs: POFile = ru_msgs
        case "EN":
            msgs: POFile = en_msgs
        case _:
            msgs: POFile = en_msgs

    try:
        del_data_dirs()
        make_dirs()
    except FileNotFoundError:
        pass
    else:
        main_logger: Logger = create_main_logger()
        action_logger: Logger = create_action_logger()

        main_logger.critical("Successful drop data")
        action_logger.critical("Successful drop data")
    finally:
        await message.answer(msgs.find("hope_msg").msgstr)
