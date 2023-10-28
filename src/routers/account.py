

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.di.shortcuts import database, current_user
from src.types.user import StandartUserWithId, PlainUser
from src.exceptions.user import username_is_occupied, user_is_unauthorized
from src.encryption.password import verify_password
from src.encryption.jwt import create_access_token
from src.types.token import Token

account_controller_router = APIRouter(tags=["AccountController"])


@account_controller_router.get("/api/Account/Me")
async def insert_user(user: current_user) -> StandartUserWithId:
    return user.get_object_without_active_status()


@account_controller_router.post("/api/Account/SignIn")
async def auth_user(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: database
) -> Token:

    if not await db.check_username_is_exists(form_data.username):
        raise user_is_unauthorized

    db_user = await db.get_user_by_name(form_data.username)

    result = verify_password(form_data.password, db_user.password)

    if not result:
        raise user_is_unauthorized

    access_token = create_access_token(
        data={"sub": form_data.username}
    )

    await db.update_user(db_user, active=True, hash_password=False)

    return Token(access_token=access_token, token_type="bearer")


@account_controller_router.post("/api/Account/SignUp")
async def register_new_user(user: PlainUser, db: database) -> StandartUserWithId:
    if await db.check_username_is_exists(user.username):
        raise username_is_occupied

    return await db.add_user(user)


@account_controller_router.post("/api/Account/SignOut")
async def sign_out_user(db: database, user: current_user) -> dict[str, bool]:
    await db.update_user(user, active=False, hash_password=False)

    return {"ok": True}


@account_controller_router.put("/api/Account/Update")
async def update_user(user: PlainUser, db: database, curr_user: current_user) -> StandartUserWithId:
    if await db.check_username_is_exists(user.username, editing_user_id=curr_user.id):
        raise username_is_occupied

    return await db.update_user(user, user_id=curr_user.id, active=False)
