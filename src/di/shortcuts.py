

from typing import Annotated

from fastapi import Depends, Query

from src.di import get_logic
from src.database.actions.logic import Logic
from src.encryption.jwt import get_current_active_user, oauth2_scheme, get_current_user_as_admin
from src.types.user import StandartUserWithId
from src.enums.rent import PriceTypes


database = Annotated[Logic, Depends(get_logic)]
current_user = Annotated[StandartUserWithId, Depends(get_current_active_user)]
admin_user = Annotated[StandartUserWithId, Depends(get_current_user_as_admin)]
token = Annotated[str, Depends(oauth2_scheme)]

rent_id_ = Annotated[int, Query(alias="rentId")]
transport_id_ = Annotated[int, Query(alias="transportId")]
rent_type_ = Annotated[PriceTypes, Query(alias="rentType")]
user_id_ = Annotated[int, Query(alias="userId")]
