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
    def get_default_user_config(user_id) -> dict[str, str | int]:
        params: dict[str, str | int] = {"id": user_id,
                                        "only_new": "on",
                                        "max_size": "10",
                                        "language": "EN",
                                        "price_filter": "on",
                                        "name_filter": "on"}
        return params
