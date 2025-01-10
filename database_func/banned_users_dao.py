from database_func.connect_to_database import DatabaseConnectionSingleton
from database_func.database_models import BannedUser


class BannedUsersDAO:
    def __init__(self):
        self.database: DatabaseConnectionSingleton = DatabaseConnectionSingleton()

    def get_banned_users(self) -> list[BannedUser]:
        query: str = '''SELECT user_id, first_name, username FROM banned_users'''
        with self.database as cursor:
            cursor.execute(query)
            banned_users_data = cursor.fetchall()

        banned_users: list[BannedUser] = [
            BannedUser(user_id=banned_user[0],
                       first_name=banned_user[1],
                       username=banned_user[2]) for banned_user in banned_users_data
        ]

        return banned_users

    def ban_user(self, banned_user: BannedUser) -> None:
        query: str = '''INSERT OR IGNORE INTO banned_users(user_id, first_name, username) VALUES(?, ?, ?)'''
        with self.database as cursor:
            cursor.execute(query, (banned_user.user_id,
                                   banned_user.first_name,
                                   banned_user.username))
        return

    def unban_user(self, user_id: int) -> None:
        query: str = '''DELETE FROM banned_users WHERE id = ?'''
        with self.database as cursor:
            cursor.execute(query, (user_id,))

        return
