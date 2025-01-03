from typing import Any
from peewee import ModelSelect
from database_func.database_objects import (
    BannedUsers,
    Users,
    UsersConfig,
    banned_users_db,
    users_config_db,
    users_db,
    admins_db,
)


class ActionsOnUsers:
    @staticmethod
    async def get_banned_users() -> list[int]:
        await banned_users_db.connect_async(reuse_if_open=True)
        banned_users_db.create_tables([BannedUsers])

        banned_users_data: ModelSelect = BannedUsers.select()
        banned_users_id: list[int] = [
            banned_user.id for banned_user in banned_users_data
        ]

        await banned_users_db.close_async()
        return banned_users_id

    @staticmethod
    async def ban_user(future_ban_user: dict[str, Any]) -> None:
        await admins_db.close_async()
        await banned_users_db.connect_async(reuse_if_open=True)
        banned_users_db.create_tables([BannedUsers])
        (BannedUsers.insert(future_ban_user).on_conflict(action="IGNORE").execute())
        banned_users_db.commit()
        await banned_users_db.close_async()

    @staticmethod
    async def unban_user(ex_ban_user: dict[str, Any]) -> bool:
        banned_users: list = await ActionsOnUsers.get_banned_users()
        if ex_ban_user["id"] not in banned_users:
            return False
        else:
            await banned_users_db.connect_async(reuse_if_open=True)
            (BannedUsers.delete().where(BannedUsers.id == ex_ban_user["id"]).execute())
            banned_users_db.commit()
            await banned_users_db.close_async()
            return True

    @staticmethod
    async def user_to_database(user_id: int, first_name: str, username: str) -> None:
        await users_db.connect_async(reuse_if_open=True)
        users_db.create_tables([Users])
        (
            Users.insert(
                {
                    "id": user_id,
                    "first_name": first_name,
                    "username": username,
                }
            )
            .on_conflict(action="IGNORE")
            .execute()
        )
        users_db.commit()
        await users_db.close_async()

    @staticmethod
    async def config_user_to_database(user_id: int) -> None:
        await users_config_db.connect_async(reuse_if_open=True)
        users_config_db.create_tables([UsersConfig])
        (
            UsersConfig.insert(
                {
                    "id": user_id,
                    "only_new": "on",
                    "max_size": "10",
                    "language": "EN",
                    "price_filter": "on",
                    "name_filter": "on"
                }
            )
            .on_conflict(action="IGNORE")
            .execute()
        )
        users_config_db.commit()
        await users_config_db.close_async()

    @staticmethod
    async def change_only_new_config(callback_data: str, user_id: int) -> None:
        only_new: str = callback_data[9:].lower()
        await users_config_db.connect_async(reuse_if_open=True)
        users_config_db.create_tables([UsersConfig])

        (
            UsersConfig.update({UsersConfig.only_new: only_new})
            .where(UsersConfig.id == user_id)
            .execute()
        )
        users_config_db.commit()
        await users_config_db.close_async()

    @staticmethod
    async def change_name_filter_config(callback_data: str, user_id: int) -> None:
        name_filter: str = callback_data[12:].lower()
        await users_config_db.connect_async(reuse_if_open=True)
        users_config_db.create_tables([UsersConfig])

        (
            UsersConfig.update({UsersConfig.name_filter: name_filter})
            .where(UsersConfig.id == user_id)
            .execute()
        )
        users_config_db.commit()
        await users_config_db.close_async()

    @staticmethod
    async def change_price_filter_config(callback_data: str, user_id: int) -> None:
        price_filter: str = callback_data[13:].lower()
        await users_config_db.connect_async(reuse_if_open=True)
        users_config_db.create_tables([UsersConfig])

        (
            UsersConfig.update({UsersConfig.price_filter: price_filter})
            .where(UsersConfig.id == user_id)
            .execute()
        )
        users_config_db.commit()
        await users_config_db.close_async()

    @staticmethod
    async def change_lang_config(callback_data: str, user_id: int) -> None:
        lang: str = callback_data[-2:]

        await users_config_db.connect_async(reuse_if_open=True)
        users_config_db.create_tables([UsersConfig])
        (
            UsersConfig.update({UsersConfig.language: lang})
            .where(UsersConfig.id == user_id)
            .execute()
        )
        users_config_db.commit()
        await users_config_db.close_async()

    @staticmethod
    async def get_all_configs(user_id: int) -> dict:
        await users_config_db.connect_async(reuse_if_open=True)

        users_config_db.create_tables([UsersConfig])
        all_config: ModelSelect = UsersConfig.select().where(UsersConfig.id == user_id)
        all_configs: UsersConfig = all_config[0]

        config_dict = {
            "only_new": all_configs.only_new,
            "max_size": all_configs.max_size,
            "language": all_configs.language,
            "price_filter": all_configs.price_filter,
            "name_filter": all_configs.name_filter
        }

        await users_config_db.close_async()
        return config_dict

    @staticmethod
    async def change_max_size_config(user_id: int, max_size: int) -> None:
        await users_config_db.connect_async(reuse_if_open=True)
        users_config_db.create_tables([UsersConfig])

        (
            UsersConfig.update({UsersConfig.max_size: max_size})
            .where(UsersConfig.id == user_id)
            .execute()
        )

        users_config_db.commit()
        await users_config_db.close_async()
