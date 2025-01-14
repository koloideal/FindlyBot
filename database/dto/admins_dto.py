from database.database_models import Admin


class AdminsDTO:
    @staticmethod
    def get_admins(admins_data: tuple) -> list[Admin]:
        admins: list[Admin] = [
            Admin(user_id=admin[0],
                  first_name=admin[1],
                  last_name=admin[2],
                  username=admin[3]) for admin in admins_data
        ]

        return admins
