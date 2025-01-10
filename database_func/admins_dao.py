from typing import Any
from database_func.connect_to_database import DatabaseConnectionSingleton


class AdminsDAO:
    def __init__(self):
        self.database: DatabaseConnectionSingleton = DatabaseConnectionSingleton()

    async def add_admin(self, user_id: int,
                        first_name: str,
                        last_name: str,
                        username: str) -> None:
        query: str = '''INSERT OR IGNORE INTO admins(user_id, first_name, last_name, username) VALUES(?, ?, ?, ?)'''
        with self.database as cursor:
            cursor.execute(query, (user_id, first_name, last_name, username))
        return

    async def del_admin(self, admin_id: int) -> None:
        query: str = '''DELETE FROM admins WHERE id = ?'''
        with self.database as cursor:
            cursor.execute(query, (admin_id,))
        return

    async def get_admins(self, only_ids: bool = True) -> list[int] | list[dict[]]:
        query: str = '''SELECT id, first_name, last_name, username FROM admins'''
        with self.database as cursor:
            cursor.execute(query)
            admins_data = cursor.fetchall()

        match only_ids:
            case True:
                admins_id: list[int] = [admin[0] for admin in admins_data]
                return admins_id
            case False:
                admins_data: list[dict[str | int]] = [
                    (admin.id, admin.first_name, admin.last_name, admin.username)
                    for admin in admins_data
                ]
                return admins_data
