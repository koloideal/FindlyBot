import logging
from aiogram.types import Message, CallbackQuery
from .database_objects import (
    BannedUsers,
    Users,
    UsersConfig,
    banned_users_db,
    users_config_db,
    users_db,
)


class ActionsOnUsers:
    @staticmethod
    async def get_banned_users() -> list:
        await banned_users_db.connect_async(reuse_if_open=True)

        banned_users_db.create_tables([BannedUsers])
        banned_users_data = BannedUsers.select()
        banned_users_id: list = [banned_user.id for banned_user in banned_users_data]

        await banned_users_db.close_async()

        return banned_users_id

    @staticmethod
    async def ban_user(message: Message, future_ban_user: dict) -> None:
        await banned_users_db.connect_async(reuse_if_open=True)

        banned_users_db.create_tables([BannedUsers])
        (BannedUsers.insert(future_ban_user).on_conflict(action="IGNORE").execute())
        banned_users_db.commit()

        await banned_users_db.close_async()

        logging.warning(f"User @{future_ban_user['username']} is banned")
        await message.answer(f"<b>@{future_ban_user['username']} is banned</b>")

    @staticmethod
    async def unban_user(message: Message, ex_ban_user: dict) -> None:
        banned_users: list = await ActionsOnUsers.get_banned_users()

        if ex_ban_user["id"] not in banned_users:
            await message.answer(f"User @{ex_ban_user['username']} was not banned")

        else:
            await banned_users_db.connect_async(reuse_if_open=True)

            (BannedUsers.delete().where(BannedUsers.id == ex_ban_user["id"]).execute())
            banned_users_db.commit()

            await banned_users_db.close_async()

            logging.warning(f"User @{ex_ban_user['username']} unbanned")
            await message.answer(f"@{ex_ban_user['username']} unbanned")

    @staticmethod
    async def user_to_database(message: Message) -> None:
        await users_db.connect_async(reuse_if_open=True)
        users_db.create_tables([Users])
        (
            BannedUsers.insert(
                {
                    "id": message.from_user.id,
                    "first_name": message.from_user.first_name,
                    "username": message.from_user.username,
                }
            )
            .on_conflict(action="IGNORE")
            .execute()
        )
        users_db.commit()
        await users_db.close_async()

        logging.warning(
            f"User @{message.from_user.username} has been added to the database or already exists in it"
        )

    @staticmethod
    async def config_user_to_database(message: Message) -> None:
        await users_config_db.connect_async(reuse_if_open=True)
        users_config_db.create_tables([UsersConfig])

        (
            UsersConfig.insert({"id": message.from_user.id})
            .on_conflict(action="IGNORE")
            .execute()
        )

        users_config_db.commit()
        await users_config_db.close_async()

    @staticmethod
    async def change_only_new_config(callback: CallbackQuery) -> None:
        user_id: int = callback.from_user.id
        only_new_serialized = {"is_only_new_OFF": True, "is_only_new_ON": False}

        await users_config_db.connect_async(reuse_if_open=True)
        users_config_db.create_tables([UsersConfig])

        (
            UsersConfig.update(
                {UsersConfig.only_new: only_new_serialized[callback.data]}
            )
            .where(UsersConfig.id == user_id)
            .execute()
        )

        users_config_db.commit()
        await users_config_db.close_async()

    @staticmethod
    async def get_user_only_new_config(user_id: int) -> bool:
        await users_config_db.connect_async(reuse_if_open=True)

        users_config_db.create_tables([UsersConfig])
        only_new = UsersConfig.select().where(UsersConfig.id == user_id)
        only_new = only_new[0].only_new

        await users_config_db.close_async()

        return only_new

    @staticmethod
    async def get_user_max_size_config(user_id: int) -> bool:
        await users_config_db.connect_async(reuse_if_open=True)

        users_config_db.create_tables([UsersConfig])
        data = UsersConfig.select().where(UsersConfig.id == user_id)
        max_size = data[0].max_size

        await users_config_db.close_async()

        return max_size

    @staticmethod
    async def change_max_size_config(message: Message) -> None:
        user_id: int = message.from_user.id
        max_size: int = int(message.text.strip())

        await users_config_db.connect_async(reuse_if_open=True)
        users_config_db.create_tables([UsersConfig])

        (
            UsersConfig.update({UsersConfig.max_size: max_size})
            .where(UsersConfig.id == user_id)
            .execute()
        )

        users_config_db.commit()
        await users_config_db.close_async()
