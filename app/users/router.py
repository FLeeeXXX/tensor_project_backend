from fastapi import APIRouter, Response, Depends
from app.exceptions import UserAlreadyExistsException
from app.users.schemas import SUsersRegister, SUsersAuth, SUsersRead, Token
from app.users.service import UsersService
from app.users.models import Users
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dependencies import get_current_user


router = APIRouter(
    prefix="/api/auth",
    tags=["Auth"]
)

# Добавить проверки на поля в регистрации
@router.post("/register")
async def register_user(user_data: SUsersRegister) -> None:
    if await UsersService.find_one_or_none(email=user_data.email): raise UserAlreadyExistsException
    await UsersService.add(login=user_data.login, email=user_data.email, password=get_password_hash(user_data.password))


# Добавить проверки на поля в авторизации
@router.post("/login")
async def login_user(user_data: SUsersAuth) -> Token:
    user = await authenticate_user(user_data.email, user_data.password)
    access_token = create_access_token({"sub": str(user.Users.id)})
    return Token(access_token=access_token)


# @router.post("/logout")
# async def logout_user(response: Response, access_token: str = Depends(get_token)) -> None:
#     response.delete_cookie("weather_access_token")


@router.get("/me")
async def get_user(user: Users = Depends(get_current_user)) -> SUsersRead:
    return user
