from fastapi import APIRouter, Response, Depends
from exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from users.schemas import SUsersRegister, SUsersAuth, SUsersRead
from users.service import UsersService
from users.models import Users
from users.auth import get_password_hash, authenticate_user, create_access_token
from users.dependencies import get_current_user


router = APIRouter(
    prefix="/api/auth",
    tags=["Auth"]
)


@router.post("/register")
async def register_user(user_data: SUsersRegister) -> None:
    existing_user = await UsersService.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersService.add(login=user_data.login, email=user_data.email, password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user_data: SUsersAuth) -> SUsersRead:
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.Users.id)})
    response.set_cookie("weather_access_token", access_token, httponly=True, samesite=None)
    return SUsersRead.from_orm(user.Users)


@router.post("/logout")
async def logout_user(responce: Response) -> None:
    responce.delete_cookie("weather_access_token")


@router.get("/me")
async def read_user_me(user: Users = Depends(get_current_user)) -> SUsersRead:
    return user
