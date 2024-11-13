from utils.make_dirs import make_dirs
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram import Bot, Dispatcher
import asyncio
from telethon import TelegramClient
import logging
from utils.get_config import GetConfig


storage: MemoryStorage = MemoryStorage()

config: dict = GetConfig.get_bot_config()
api_token: str = config["Config"]["test_api_token"]

api_id: int = int(config["Settings"]["api_id"])
api_hash: str = config["Settings"]["api_hash"]

client: TelegramClient = TelegramClient("session", api_id, api_hash)
client.start()
client.disconnect()

bot: Bot = Bot(token=api_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp: Dispatcher = Dispatcher(storage=storage)


async def main() -> None:
    await make_dirs()
    from handlers.routers import router

    logging.warning("Starting FindlyBot...")
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        print("\n\033[1m\033[30m\033[44m {} \033[0m".format("Starting FindlyBot..."))

        logger = logging.getLogger(__name__)
        logging.basicConfig(
            level=logging.WARNING,
            filename="secret_data/logs.log",
            filemode="a",
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s\n\n\n",
        )

        asyncio.run(main())

    except KeyboardInterrupt:
        print("\n\033[1m\033[30m\033[45m {} \033[0m".format("End of work..."))

        logging.warning("End of work...")

        exit()
