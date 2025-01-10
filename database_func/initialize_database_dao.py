from database_func.connect_to_database import DatabaseConnectionSingleton


class InitializeDatabaseDAO:
    def __init__(self):
        self.database: DatabaseConnectionSingleton = DatabaseConnectionSingleton()

    def create_tables(self) -> None:
        table_create_queries: list[str] = ['''CREATE TABLE IF NOT EXISTS config_users(user_id INTEGER NOT NULL UNIQUE, only_new VARCHAR(3), max_size INTEGER, name_filter VARCHAR(3), price_filter VARCHAR(3), language VARCHAR(2))''',
                                           '''CREATE TABLE IF NOT EXISTS users(user_id INTEGER NOT NULL UNIQUE, first_name VARCHAR(50), username VARCHAR(50))''',
                                           '''CREATE TABLE IF NOT EXISTS banned_users(user_id INTEGER NOT NULL UNIQUE, first_name VARCHAR(50), username VARCHAR(50))''',
                                           '''CREATE TABLE IF NOT EXISTS admins(user_id INTEGER NOT NULL UNIQUE, first_name VARCHAR(50), last_name VARCHAR(50), username VARCHAR(50))''']
        with self.database as cursor:
            for table_create_query in table_create_queries:
                cursor.execute(table_create_query)

        return

    @staticmethod
    def create_database(**kwargs) -> None:
        connection: DatabaseConnectionSingleton = DatabaseConnectionSingleton(**kwargs)
        query: str = '''CREATE DATABASE IF NOT EXISTS FindlyBot'''

        with connection as cursor:
            cursor.execute(query)

        DatabaseConnectionSingleton.__del__()

        return
