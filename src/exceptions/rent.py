

from fastapi import status, HTTPException


its_not_user_rent = HTTPException(
    status.HTTP_403_FORBIDDEN,
    detail="You are not a owner or renter of this transport"
)


rent_self_ransport = HTTPException(
    status.HTTP_403_FORBIDDEN,
    detail="You cant rent a transport which you are owner"
)


undefined_rent_type = HTTPException(
    status.HTTP_400_BAD_REQUEST,
    detail="Undefined rent type"
)


transport_is_busy = HTTPException(
    status.HTTP_400_BAD_REQUEST,
    detail="This transport is busy"
)

rent_is_already_finish = HTTPException(
    status.HTTP_400_BAD_REQUEST,
    detail="This transport is already finish"
)


its_not_your_rent = HTTPException(
    status.HTTP_400_BAD_REQUEST,
    detail="It's not your rent"
)


undefined_rent = HTTPException(
    status.HTTP_400_BAD_REQUEST,
    detail="Rent with this id is undefined"
)
