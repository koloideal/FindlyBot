class Admin:
    def __init__(self, user_id: int,
                 first_name: str,
                 last_name: str,
                 username: str):
        self.user_id: int = user_id
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.username: str = username


class User:
    def __init__(self, user_id: int,
                 first_name: str,
                 username: str):
        self.user_id: int = user_id
        self.first_name: str = first_name
        self.username: str = username


class BannedUser:
    def __init__(self, user_id: int,
                 first_name: str,
                 username: str):
        self.user_id: int = user_id
        self.first_name: str = first_name
        self.username: str = username


class UserConfig:
    def __init__(self, user_id: int,
                 only_new: str,
                 max_size: int,
                 language: str,
                 price_filter: str,
                 name_filter: str):
        self.user_id: int = user_id
        self.only_new: str = only_new
        self.max_size: int = max_size
        self.language: str = language
        self.price_filter: str = price_filter
        self.name_filter: str = name_filter

    @staticmethod
    def get_default_user_config(user_id) -> tuple:
        params:tuple = (user_id, "on", 10, "EN", "on", "on")
        return params


class SerializerDatabaseModels:
    @staticmethod
    def admins_serialize(list_of_admins: list[Admin]) -> dict[str, list]:
        admins_dict: dict[str, list] = {'admins': []}
        for admin in list_of_admins:
            admins_dict['admins'].append({
                'user_id': admin.user_id,
                'first_name': admin.first_name,
                'last_name': admin.last_name,
                'username': admin.username
            })

        return admins_dict

    @staticmethod
    def users_serialize(list_of_users: list[User]) -> dict[str, list]:
        users_dict: dict[str, list] = {'users': []}
        for user in list_of_users:
            users_dict['users'].append({
                'user_id': user.user_id,
                'first_name': user.first_name,
                'username': user.username
            })

        return users_dict

    @staticmethod
    def banned_users_serialize(list_of_banned_users: list[BannedUser]) -> dict[str, list]:
        banned_users_dict: dict[str, list] = {'banned_users': []}
        for banned_user in list_of_banned_users:
            banned_users_dict['banned_users'].append({
                'user_id': banned_user.user_id,
                'first_name': banned_user.first_name,
                'username': banned_user.username
            })

        return banned_users_dict
