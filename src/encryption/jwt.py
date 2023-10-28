

from typing import Annotated
from datetime import timedelta, datetime

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt

from src.types.token import TokenData
from src.exceptions.user import user_is_unauthorized, inactive_user
from src.database.actions.logic import Logic
from src.di.db import get_logic
from src.types.user import UserWithActive

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "0241f86f3d997180b13fcbee406b0357957303ce95db18133fb0702a864086fe"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/Account/SignIn")

EXPIRES_DELTA = timedelta(minutes=30)


def create_access_token(data: dict, expires_delta: timedelta = EXPIRES_DELTA) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Annotated[Logic, Depends(get_logic)]
) -> UserWithActive:

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise user_is_unauthorized
        token_data = TokenData(username=username)

    except JWTError:
        raise user_is_unauthorized

    try:
        user = await db.get_user_by_name(user_name=token_data.username)

    except (IndexError, AttributeError):
        raise user_is_unauthorized

    if user is None:
        raise user_is_unauthorized
    return user


async def get_current_active_user(
    current_user: Annotated[UserWithActive, Depends(get_current_user)]
) -> UserWithActive:

    if not current_user.active:
        raise inactive_user

    return current_user
