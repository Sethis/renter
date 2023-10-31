

from fastapi import status, HTTPException


undefined_transport = HTTPException(
    status.HTTP_400_BAD_REQUEST,
    detail="Undefined transport"
)


its_not_user_transport = HTTPException(
    status.HTTP_403_FORBIDDEN,
    detail="You are not the owner of this transport"
)

undefined_type = HTTPException(
    status.HTTP_400_BAD_REQUEST,
    detail="The transport type is uncorrect"
)
