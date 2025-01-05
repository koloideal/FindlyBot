from logging import Logger
from utils.make_dirs import make_dirs
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram import Bot, Dispatcher
import asyncio
from telethon import TelegramClient
from utils.get_config import GetConfig
from utils.create_loggers import create_main_logger, create_action_logger


config: dict = GetConfig.get_bot_config()
api_token: str = config["Config"]["test_api_token"]
api_id: int = int(config["Settings"]["api_id"])
api_hash: str = config["Settings"]["api_hash"]

client: TelegramClient = TelegramClient("session", api_id, api_hash).start()
client.disconnect()

bot: Bot = Bot(token=api_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage: MemoryStorage = MemoryStorage()
dp: Dispatcher = Dispatcher(storage=storage)

main_logger: Logger = create_main_logger()
action_logger: Logger = create_action_logger()


async def main() -> None:
    await make_dirs()
    from handlers.routers import router

    main_logger.warning("Starting FindlyBot...")
    action_logger.critical("Starting logging actions...")
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

    print("\n\033[1m\033[30m\033[45m {} \033[0m".format("End of work..."))
    main_logger.warning("End of work...")
    action_logger.critical("End of logging actions...")
    exit()

if __name__ == "__main__":
    print("\n\033[1m\033[30m\033[44m {} \033[0m".format("Starting FindlyBot..."))
    asyncio.run(main())
