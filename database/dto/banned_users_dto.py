from database.database_models import BannedUser


class BannedUsersDTO:
    @staticmethod
    def get_admins(banned_users_data: tuple) -> list[BannedUser]:
        banned_users: list[BannedUser] = [
            BannedUser(user_id=banned_user[0],
                       first_name=banned_user[1],
                       username=banned_user[2]) for banned_user in banned_users_data
        ]

        return banned_users
