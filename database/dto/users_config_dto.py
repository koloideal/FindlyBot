from database.database_models import UserConfig


class UsersConfigDTO:
    @staticmethod
    def get_all_configs(config: tuple, user_id: int) -> UserConfig:
        user_config = UserConfig(
            user_id=user_id,
            only_new=config[0],
            max_size=config[1],
            language=config[2],
            price_filter=config[3],
            name_filter=config[4]
        )

        return user_config
