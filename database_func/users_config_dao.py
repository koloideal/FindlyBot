from .connect_to_database import DatabaseConnectionSingleton


class UsersConfigDAO:
    def __init__(self):
        self.database: DatabaseConnectionSingleton = DatabaseConnectionSingleton()

    async def config_user_to_database(self, user_id: int) -> None:
        query: str = '''INSERT OR IGNORE INTO 
                        users_config(id, only_new, max_size, language, price_filter, name_filter) 
                        VALUES(?, ?, ?, ?, ?, ?)'''

        params: dict[int | str, str] = {"id": user_id,
                                        "only_new": "on",
                                        "max_size": "10",
                                        "language": "EN",
                                        "price_filter": "on",
                                        "name_filter": "on"}
        with self.database as cursor:
            cursor.execute(query, params)

        return

    async def change_only_new_config(self, callback_data: str, user_id: int) -> None:
        only_new: str = callback_data.split('_')[-1].lower()

        query: str = '''UPDATE users_config SET only_new = ? WHERE user_id = ?'''

        with self.database as cursor:
            cursor.execute(query, (only_new, user_id))

    async def change_name_filter_config(self, callback_data: str, user_id: int) -> None:
        name_filter: str = callback_data.split('_')[-1].lower()

        query: str = '''UPDATE users_config SET name_filter = ? WHERE user_id = ?'''

        with self.database as cursor:
            cursor.execute(query, (name_filter, user_id))

    async def change_price_filter_config(self, callback_data: str, user_id: int) -> None:
        price_filter: str = callback_data.split('_')[-1].lower()

        query: str = '''UPDATE users_config SET price_filter = ? WHERE user_id = ?'''

        with self.database as cursor:
            cursor.execute(query, (price_filter, user_id))

    async def change_lang_config(self, callback_data: str, user_id: int) -> None:
        language: str = callback_data.split('_')[-1]

        query: str = '''UPDATE users_config SET language = ? WHERE user_id = ?'''

        with self.database as cursor:
            cursor.execute(query, (language, user_id))

    async def get_all_configs(self, user_id: int) -> dict:
        query: str = '''SELECT only_new, max_size, language, price_filter, name_filter FROM users_config WHERE user_id = ?'''

        with self.database as cursor:
            cursor.execute(query, (user_id,))
            config = cursor.fetchone()

        config_dict = {
            "only_new": config[0],
            "max_size": config[1],
            "language": config[2],
            "price_filter": config[3],
            "name_filter": config[4]
        }

        return config_dict

    async def change_max_size_config(self, user_id: int, max_size: int) -> None:
        query: str = '''UPDATE users_config SET max_size = ? WHERE user_id = ?'''

        with self.database as cursor:
            cursor.execute(query, (max_size, user_id))
