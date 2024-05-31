from fastapi import HTTPException, status


class UnauthorizedException(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class UnprocessableContentException(HTTPException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class ConflictException(HTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class ServerException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class IncorrectEmailOrPasswordException(UnauthorizedException):
    detail = "Неверная почта или пароль"


class UserAlreadyExistsException(ConflictException):
    detail = "Пользователь уже существует"


class TokenExpiredException(UnauthorizedException):
    detail = "Токен истек"


class TokenAbsentException(UnauthorizedException):
    detail = "Токен отсутствует"


class IncorrectTokenFormatException(UnprocessableContentException):
    detail = "Не верный формат токена"


class UserNotFoundException(UnauthorizedException):
    detail = ""


class ServerNetworkException(ServerException):
    detail = "Внутренняя ошибка сервера"


class IncorrectDataException(UnprocessableContentException):
    detail = "Не верный формат данных"
