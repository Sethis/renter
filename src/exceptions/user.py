

from fastapi import status, HTTPException


username_is_occupied = HTTPException(
    status.HTTP_400_BAD_REQUEST,
    detail="The username is occupied"
)


user_is_unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials. Please try logging in again",
        headers={"WWW-Authenticate": "Bearer"},
)

user_is_undefined = HTTPException(
    status.HTTP_400_BAD_REQUEST,
    detail="This user is undefined"
)

forrbiden_result = HTTPException(
    status.HTTP_403_FORBIDDEN,
    detail="Denial of access"
)


inactive_user = HTTPException(status_code=400, detail="Inactive user")
