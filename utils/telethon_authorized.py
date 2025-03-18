from logging import Logger, getLogger
from telethon import TelegramClient
from tomlkit import load, dump


action_logger: Logger = getLogger('action_logger')

async def telethon_authorized(api_id, api_hash):
    client = TelegramClient("session", api_id=api_id, api_hash=api_hash)

    with open("secret_data/config.toml", "rb") as config:
        config = load(config)

    two_factor_auth_password = config["Bot"]["Settings"]["two_factor_auth_password"]

    if two_factor_auth_password:
        await client.start(password=two_factor_auth_password)
    else:
        await client.start()
    await client.get_me()
    await client.disconnect()

    config["Bot"]["Config"]["is_authorized"] = True
    with open("secret_data/config.toml", "w") as modified_config:
        dump(config, modified_config)

    action_logger.critical("Successfully authorized in telethon")
