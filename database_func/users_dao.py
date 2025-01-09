from .connect_to_database import DatabaseConnectionSingleton


class UsersDAO:
    def __init__(self):
        self.database: DatabaseConnectionSingleton = DatabaseConnectionSingleton()

    async def user_to_database(self,
                               user_id: int,
                               first_name: str,
                               username: str) -> None:

        query: str = '''INSERT OR IGNORE INTO users(user_id, first_name, username) VALUES(?, ?, ?)'''
        with self.database as cursor:
            cursor.execute(query, (user_id, first_name, username))

        return
