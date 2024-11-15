class InvalidUsernameForBan(Exception):
    def __init__(self, invalid_username):
        self.__invalid_username = invalid_username

    def __str__(self):
        return f"Invalid username for ban: {self.__invalid_username}"


class InvalidUsernameForUnban(Exception):
    def __init__(self, invalid_username):
        self.__invalid_username = invalid_username

    def __str__(self):
        return f"Invalid username for unban: {self.__invalid_username}"


class AttemptToBanAdminOrCreator(Exception):
    def __init__(self, invalid_username):
        self.__invalid_username = invalid_username

    def __str__(self):
        return f"You can't ban a '{self.__invalid_username}' since he is an admin or creator"


class InvalidUsernameForAddAdmin(Exception):
    def __init__(self, invalid_username):
        self.__invalid_username = invalid_username

    def __str__(self):
        return f"Invalid username for add admin: {self.__invalid_username}"
