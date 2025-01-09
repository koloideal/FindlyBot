from database_func.connect_to_database import DatabaseConnectionSingleton


class BannedUsersDAO:
    def __init__(self):
        self.database: DatabaseConnectionSingleton = DatabaseConnectionSingleton()

    def get_banned_users(self) -> list[int]:
        query: str = '''SELECT id FROM banned_users'''
        with self.database as cursor:
            cursor.execute(query)
            banned_users_id = cursor.fetchall()

        banned_users_id = [x[0] for x in banned_users_id]

        return banned_users_id

    def ban_user(self,
                       user_id: int,
                       first_name: str,
                       username: str) -> None:
        query: str = '''INSERT OR IGNORE INTO banned_users(user_id, first_name, username) VALUES(?, ?, ?)'''
        with self.database as cursor:
            cursor.execute(query, (user_id, first_name, username))

        return

    def unban_user(self, user_id: int) -> bool:
        banned_users: list[int] = BannedUsersDAO().get_banned_users()
        if user_id not in banned_users:
            return False
        else:
            query: str = '''DELETE FROM banned_users WHERE id = ?'''
            with self.database as cursor:
                cursor.execute(query, (user_id,))
            return True
