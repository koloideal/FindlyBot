import tomllib


class GetConfig:
    @staticmethod
    def get_api_config() -> dict:
        with open("secret_data/config.toml", "rb") as config:
            config = tomllib.load(config)["API"]

        return config

    @staticmethod
    def get_bot_config() -> dict:
        with open("secret_data/config.toml", "rb") as config:
            config = tomllib.load(config)["Bot"]

        return config
