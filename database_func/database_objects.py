from peewee import Model, IntegerField, CharField
from aiopeewee import SqliteDatabaseAsync


banned_users_db: SqliteDatabaseAsync = SqliteDatabaseAsync(
    "database/banned_users.sqlite3", autoconnect=False
)
users_config_db: SqliteDatabaseAsync = SqliteDatabaseAsync(
    "database/users_config.sqlite3", autoconnect=False
)
users_db: SqliteDatabaseAsync = SqliteDatabaseAsync(
    "database/users.sqlite3", autoconnect=False
)


class BannedUsers(Model):
    id: IntegerField = IntegerField(unique=True)
    first_name: CharField = CharField(max_length=50, null=True)
    last_name: CharField = CharField(max_length=50, null=True)
    username: CharField = CharField(max_length=50, null=True)

    class Meta:
        database: SqliteDatabaseAsync = banned_users_db
        db_table: str = "banned_users"


class Users(Model):
    id: IntegerField = IntegerField(unique=True)
    first_name: CharField = CharField(max_length=50, null=True)
    username: CharField = CharField(max_length=50, null=True)

    class Meta:
        database: SqliteDatabaseAsync = users_db
        db_table: str = "users"


class UsersConfig(Model):
    id: IntegerField = IntegerField(unique=True)
    only_new: CharField = CharField(default="on")
    max_size: IntegerField = IntegerField(default=10)
    name_filter: CharField = CharField(default="on")
    price_filter: CharField = CharField(default="on")
    language: CharField = CharField(default="EN", max_length=2)

    class Meta:
        database: SqliteDatabaseAsync = users_config_db
        db_table: str = "config_users"


admins_db: SqliteDatabaseAsync = SqliteDatabaseAsync(
    "database/admins.sqlite3", autoconnect=False
)


class AdminUsers(Model):
    id: IntegerField = IntegerField(unique=True)
    first_name: CharField = CharField(max_length=50, null=True)
    last_name: CharField = CharField(max_length=50, null=True)
    username: CharField = CharField(max_length=50, null=True)

    class Meta:
        database: SqliteDatabaseAsync = admins_db
        db_table: str = "admin_users"
