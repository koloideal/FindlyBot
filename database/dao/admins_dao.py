from database.connect_to_database import DatabaseConnectionSingleton
from database.database_models import Admin


class AdminsDAO:
    def __init__(self):
        self.database: DatabaseConnectionSingleton = DatabaseConnectionSingleton()

    def add_admin(self, admin: Admin) -> None:
        query: str = '''INSERT IGNORE INTO admins(user_id, first_name, last_name, username) VALUES(?, ?, ?, ?)'''
        with self.database as cursor:
            cursor.execute(query, (admin.user_id,
                                   admin.first_name,
                                   admin.last_name,
                                   admin.username))

        return

    def del_admin(self, admin_id: int) -> None:
        query: str = '''DELETE FROM admins WHERE user_id = ?'''
        with self.database as cursor:
            cursor.execute(query, (admin_id,))

        return

    def get_admins(self) -> list[Admin]:
        query: str = '''SELECT user_id, first_name, last_name, username FROM admins'''
        with self.database as cursor:
            cursor.execute(query)
            admins_data = cursor.fetchall()

        admins: list[Admin] = [
            Admin(user_id = admin[0],
                  first_name = admin[1],
                  last_name = admin[2],
                  username = admin[3]) for admin in admins_data
        ]

        return admins
