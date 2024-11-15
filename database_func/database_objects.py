from peewee import Model, IntegerField, CharField, BooleanField
from aiopeewee import SqliteDatabaseAsync


banned_users_db = SqliteDatabaseAsync("database/banned_users.sqlite3", autoconnect=False)
users_config_db = SqliteDatabaseAsync("database/users_config.sqlite3", autoconnect=False)
users_db = SqliteDatabaseAsync("database/users.sqlite3", autoconnect=False)


class BannedUsers(Model):
    id = IntegerField(unique=True)
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    username = CharField(max_length=50)

    class Meta:
        database = banned_users_db
        db_table = "banned_users"


class Users(Model):
    id = IntegerField(unique=True)
    first_name = CharField(max_length=50)
    username = CharField(max_length=50)

    class Meta:
        database = users_db
        db_table = "users"


class UsersConfig(Model):
    id = IntegerField(unique=True)
    only_new = BooleanField(default=False)
    max_size = IntegerField(default=10)

    class Meta:
        database = users_config_db
        db_table = "config_users"


admins_db = SqliteDatabaseAsync("database/admins.sqlite3", autoconnect=False)


class AdminUsers(Model):
    id = IntegerField(unique=True)
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    username = CharField(max_length=50)

    class Meta:
        database = admins_db
        db_table = "admin_users"
