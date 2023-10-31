

from fastapi import APIRouter

from src.di.shortcuts import database, current_user
from src.types.user import StandartUserWithId
from src.exceptions.user import forrbiden_result, user_is_undefined


payments_controller_router = APIRouter(tags=["PaymentController"])


@payments_controller_router.post("/api/Payment/Hesoyam/{account_id}")
async def make_user_to_admin(account_id: int, user: current_user, db: database) -> StandartUserWithId:
    if not user.isAdmin and account_id != user.id:
        raise forrbiden_result

    if not await db.check_user_is_exists(account_id):
        raise user_is_undefined

    db_user = await db.get_user_by_id(account_id)

    db_user.balance += 250000

    result = await db.update_user(db_user, hash_password=False)

    return result
