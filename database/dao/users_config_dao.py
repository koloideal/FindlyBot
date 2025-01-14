from database.connect_to_database import DatabaseConnectionSingleton
from database.database_models import UserConfig
from database.dto.users_config_dto import UsersConfigDTO


class UsersConfigDAO:
    def __init__(self):
        self.database: DatabaseConnectionSingleton = DatabaseConnectionSingleton()

    def config_user_to_database(self, params: tuple) -> None:
        query: str = '''INSERT IGNORE INTO users_config(user_id, only_new, max_size, language, price_filter, name_filter) VALUES(?, ?, ?, ?, ?, ?)'''
        with self.database as cursor:
            cursor.execute(query, params)

        return

    def change_only_new_config(self, only_new: str, user_id: int) -> None:
        query: str = '''UPDATE users_config SET only_new = ? WHERE user_id = ?'''
        with self.database as cursor:
            cursor.execute(query, (only_new, user_id))

    def change_name_filter_config(self, name_filter: str, user_id: int) -> None:
        query: str = '''UPDATE users_config SET name_filter = ? WHERE user_id = ?'''
        with self.database as cursor:
            cursor.execute(query, (name_filter, user_id))

        return

    def change_price_filter_config(self, price_filter: str, user_id: int) -> None:
        query: str = '''UPDATE users_config SET price_filter = ? WHERE user_id = ?'''
        with self.database as cursor:
            cursor.execute(query, (price_filter, user_id))

        return

    def change_lang_config(self, language: str, user_id: int) -> None:
        query: str = '''UPDATE users_config SET language = ? WHERE user_id = ?'''
        with self.database as cursor:
            cursor.execute(query, (language, user_id))

        return

    def get_all_configs(self, user_id: int) -> UserConfig:
        query: str = '''SELECT only_new, max_size, language, price_filter, name_filter FROM users_config WHERE user_id = ?'''
        with self.database as cursor:
            cursor.execute(query, (user_id,))
            config = cursor.fetchone()

        return UsersConfigDTO.get_all_configs(config=config, user_id=user_id)

    def change_max_size_config(self, user_id: int, max_size: int) -> None:
        query: str = '''UPDATE users_config SET max_size = ? WHERE user_id = ?'''
        with self.database as cursor:
            cursor.execute(query, (max_size, user_id))

        return
