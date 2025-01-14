from database.connect_to_database import DatabaseConnectionSingleton
from database.database_models import BannedUser
from database.dto.banned_users_dto import BannedUsersDTO


class BannedUsersDAO:
    def __init__(self):
        self.database: DatabaseConnectionSingleton = DatabaseConnectionSingleton()

    def get_banned_users(self) -> list[BannedUser]:
        query: str = '''SELECT user_id, first_name, username FROM banned_users'''
        with self.database as cursor:
            cursor.execute(query)
            banned_users_data = cursor.fetchall()

        return BannedUsersDTO.get_admins(banned_users_data=banned_users_data)

    def ban_user(self, banned_user: BannedUser) -> None:
        query: str = '''INSERT IGNORE INTO banned_users(user_id, first_name, username) VALUES(?, ?, ?)'''
        with self.database as cursor:
            cursor.execute(query, (banned_user.user_id,
                                   banned_user.first_name,
                                   banned_user.username))
        return

    def unban_user(self, user_id: int) -> None:
        query: str = '''DELETE FROM banned_users WHERE user_id = ?'''
        with self.database as cursor:
            cursor.execute(query, (user_id,))

        return
