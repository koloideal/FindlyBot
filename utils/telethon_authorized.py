from logging import Logger, getLogger
from telethon import TelegramClient
from tomlkit import load, dump


action_logger: Logger = getLogger('action_logger')

async def telethon_authorized(api_id, api_hash):
    client = TelegramClient("session", api_id=api_id, api_hash=api_hash)

    await client.start()
    await client.get_me()
    await client.disconnect()

    with open("secret_data/config.toml", "rb") as config:
        config = load(config)
    config["Bot"]["Config"]["is_authorized"] = True
    with open("secret_data/config.toml", "w") as modified_config:
        dump(config, modified_config)

    action_logger.critical("Successfully authorized in telethon")
