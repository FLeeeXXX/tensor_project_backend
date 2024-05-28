from jose import jwt
from datetime import datetime, timedelta
from pydantic import EmailStr
from passlib.context import CryptContext
from app.users.service import UsersService
from app.config import settings
from app.exceptions import IncorrectEmailOrPasswordException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.HASH_ALGORITHM
    )
    return encoded_jwt, expire

async def authenticate_user(email: EmailStr, password: str):
    user = await UsersService.find_one_or_none(email=email)
    if (not user) or (not verify_password(password, user.Users.password)):
        raise IncorrectEmailOrPasswordException
    return user
    