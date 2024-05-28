from fastapi import APIRouter, Response, Depends
from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from app.users.schemas import SUsersRegister, SUsersAuth, SUsersRead
from app.users.service import UsersService
from app.users.models import Users
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dependencies import get_current_user, get_token


router = APIRouter(
    prefix="/api/auth",
    tags=["Auth"]
)

# Добавить проверки на поля в регистрации
@router.post("/register")
async def register_user(user_data: SUsersRegister) -> None:
    existing_user = await UsersService.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersService.add(login=user_data.login, email=user_data.email, password=hashed_password)

# Добавить проверки на поля в авторизации
@router.post("/login")
async def login_user(response: Response, user_data: SUsersAuth) -> SUsersRead:
    user = await authenticate_user(user_data.email, user_data.password)
    access_token, expire = create_access_token({"sub": str(user.Users.id)})
    response.set_cookie("weather_access_token", access_token, secure=True, httponly=True, samesite='none', expires=expire.strftime("%a, %d %b %Y %H:%M:%S GMT"))
    return SUsersRead.from_orm(user.Users)

# Может подправить логику
@router.post("/logout")
async def logout_user(responce: Response) -> None:
    if get_token(responce):
        responce.delete_cookie("weather_access_token")


@router.get("/me")
async def read_user_me(user: Users = Depends(get_current_user)) -> SUsersRead:
    return user
