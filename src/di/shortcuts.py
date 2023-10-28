

from typing import Annotated

from fastapi import Depends

from src.di import get_logic
from src.database.actions.logic import Logic
from src.encryption.jwt import get_current_active_user
from src.types.user import UserWithActive

database = Annotated[Logic, Depends(get_logic)]

current_user = Annotated[UserWithActive, Depends(get_current_active_user)]
