from fastapi import Request, Depends
from exceptions import TokenExpiredException, TokenAbsentException, IncorrectTokenFormatException, UserNotFoundException
from jose import jwt, JWTError
from config import settings
from datetime import datetime
from users.service import UsersService
from users.schemas import SUsersRead


def get_token(request: Request) -> str:
    token = request.cookies.get("booking_access_token")
    if token == None:
        raise TokenAbsentException
    return token


async def get_current_user(access_token: str = Depends(get_token)) -> SUsersRead:
    try:
        payload = jwt.decode(
            access_token,  settings.SECRET_KEY, settings.HASH_ALGORITHM
        )
    except JWTError:
        raise IncorrectTokenFormatException

    expire: str = payload.get("exp")

    if (not expire) or (int(expire) < datetime.utcnow().timestamp()): 
        raise TokenExpiredException
    user_id: str = payload.get("sub")

    if not user_id:
        raise UserNotFoundException
    
    user = await UsersService.find_by_id(int(user_id))
    if not user:
        raise UserNotFoundException

    return SUsersRead.from_orm(user.Users)
