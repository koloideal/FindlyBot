from typing import Any
from .database_objects import AdminUsers, admins_db
from peewee import ModelSelect


class ActionsOnAdmin:
    @staticmethod
    async def add_admin(future_admin: dict[str, Any]) -> None:
        await admins_db.connect_async(reuse_if_open=True)
        admins_db.create_tables([AdminUsers])
        admins_db.commit()
        (
            AdminUsers
            .insert(future_admin)
            .execute()
        )
        admins_db.commit()
        await admins_db.close_async()


    @staticmethod
    async def del_admin(ex_admin: dict[str, Any]) -> None:
        await admins_db.connect_async(reuse_if_open=True)
        (
            AdminUsers
            .delete()
            .where(AdminUsers.id == ex_admin["id"])
            .execute()
        )
        admins_db.commit()
        await admins_db.close_async()

    @staticmethod
    async def get_admins(only_ids: bool = True) -> list[int] | list[tuple]:
        await admins_db.connect_async(reuse_if_open=True)
        admins_db.create_tables([AdminUsers])
        data: ModelSelect = AdminUsers.select()
        match only_ids:
            case True:
                admins_id: list[int] = [admin.id for admin in data]
                return admins_id
            case False:
                admins_data: list[tuple] = [(admin.id, admin.first_name, admin.last_name, admin.username)
                                     for admin in data]
                return admins_data

        await admins_db.close_async()
