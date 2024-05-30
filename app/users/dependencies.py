from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.exceptions import TokenExpiredException, TokenAbsentException, IncorrectTokenFormatException, UserNotFoundException
from jose import jwt, JWTError
from app.config import settings
from datetime import datetime
from app.users.service import UsersService
from app.users.schemas import SUsersRead


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(access_token: str = Depends(oauth2_scheme)) -> SUsersRead:
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
