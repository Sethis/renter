

from fastapi import APIRouter

from src.di.shortcuts import database, admin_user, current_user
from src.types.user import StandartUserWithId, StandartUser
from src.exceptions.user import username_is_occupied, user_is_undefined


admin_account_controller_router = APIRouter(tags=["AdminAccountController"])


@admin_account_controller_router.post("/api/Admin/BAGUVIX")
async def make_user_to_admin(user: current_user, db: database) -> StandartUserWithId:
    user.isAdmin = True

    result = await db.update_user(user, hash_password=False)

    return result


@admin_account_controller_router.get("/api/Admin/Account")
async def admin_get_all_users(
        start: int,
        count: int,
        _admin: admin_user,
        db: database
) -> list[StandartUserWithId]:

    return await db.get_all_users(start=start, count=count)


@admin_account_controller_router.get("/api/Admin/Account/{id}")
async def admin_get_user_by_id(id: int, _admin: admin_user, db: database) -> StandartUserWithId:
    if not await db.check_user_is_exists(id):
        raise user_is_undefined

    result = await db.get_user_by_id(id)

    return result


@admin_account_controller_router.post("/api/Admin/Account")
async def admin_insert_user(user: StandartUser, db: database, _admin: admin_user) -> StandartUserWithId:
    if await db.check_username_is_exists(user.username):
        raise username_is_occupied

    return await db.add_user(user)


@admin_account_controller_router.put("/api/Admin/Account/{id}")
async def admin_edit_user_by_id(
        id: int, user: StandartUser, db: database, _admin: admin_user
) -> StandartUserWithId:

    if await db.check_username_is_exists(user.username, editing_user_id=id):
        raise username_is_occupied

    if not await db.check_user_is_exists(id):
        raise user_is_undefined

    return await db.update_user(user, user_id=id)


@admin_account_controller_router.delete("/api/Admin/Account/{id}")
async def admin_delete_user_by_id(id: int, db: database, _admin: admin_user) -> dict[str, bool]:
    if not await db.check_user_is_exists(id):
        raise user_is_undefined

    await db.delete_user_by_id(id)

    return {"ok": True}
