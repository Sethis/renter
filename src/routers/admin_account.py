

from fastapi import APIRouter

from src.di.shortcuts import database, current_user
from src.types.user import StandartUserWithId, StandartUser
from src.exceptions.user import forrbiden_result, username_is_occupied, user_is_undefined


admin_account_controller_router = APIRouter(tags=["AdminAccountController"])


@admin_account_controller_router.post("/api/Admin/BAGUVIX")
async def make_user_to_admin(user: current_user, db: database) -> StandartUserWithId:
    user.isAdmin = True

    result = await db.update_user(user, hash_password=False)

    return result.get_object_without_active_status()


@admin_account_controller_router.get("/api/Admin/Account")
async def admin_get_all_users(start: int, count: int, user: current_user, db: database) -> list[StandartUserWithId]:
    if not user.isAdmin:
        raise forrbiden_result

    return await db.get_all_users(start=start, count=count)


@admin_account_controller_router.get("/api/Admin/Account/{ido}")
async def admin_get_user_by_id(ido: int, user: current_user, db: database) -> StandartUserWithId:
    if not user.isAdmin:
        raise forrbiden_result

    if not await db.check_user_is_exists(ido):
        raise user_is_undefined

    result = await db.get_user_by_id(ido)

    return result.get_object_without_active_status()


@admin_account_controller_router.post("/api/Admin/Account")
async def admin_insert_user(user: StandartUser, db: database, curr_user: current_user) -> StandartUserWithId:
    if not curr_user.isAdmin:
        raise forrbiden_result

    if await db.check_username_is_exists(user.username):
        raise username_is_occupied

    return await db.add_user(user)


@admin_account_controller_router.put("/api/Admin/Account/{ido}")
async def admin_edit_user_by_id(ido: int, user: StandartUser, db: database, curr_user: current_user) -> StandartUserWithId:
    if not curr_user.isAdmin:
        raise forrbiden_result

    if await db.check_username_is_exists(user.username, editing_user_id=ido):
        raise username_is_occupied

    if not await db.check_user_is_exists(ido):
        raise user_is_undefined

    return await db.update_user(user, user_id=ido)


@admin_account_controller_router.delete("/api/Admin/Account/{ido}")
async def admin_delete_user_by_id(ido: int, db: database, curr_user: current_user) -> dict[str, bool]:
    if not curr_user.isAdmin:
        raise forrbiden_result

    if not await db.check_user_is_exists(ido):
        raise user_is_undefined

    await db.delete_user_by_id(ido)

    return {"ok": True}