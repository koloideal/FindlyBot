from peewee import *
import random

users_config_db = SqliteDatabase('database/urytjhgkksrs.sqlite3')

class UsersConfig(Model):
    id = IntegerField(unique=True)
    only_new = BooleanField(default=False)
    max_size = IntegerField(default=10)

    class Meta:
        database = users_config_db
        db_table = 'config_users'

users_config_db.connect()
users_config_db.create_tables([UsersConfig])

'''for i in [random.randint(1, 1000) for x in range(1000)]:
    user = (
            BannedUsers
            .insert({'id': i,
                    'first_name': 'John' + str(i),
                    'last_name': 'Doe' + str(i),
                    'username': '@Joh' + str(i)})
            .on_conflict(action='IGNORE')
            .execute()
            )

    db.commit()

print([x.id for x in BannedUsers.select()])'''

only_new = UsersConfig.select().where(UsersConfig.id == 12345)
print(only_new[0].only_new)

users_config_db.commit()


