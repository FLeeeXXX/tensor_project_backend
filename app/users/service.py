from service.base import BaseService
from users.models import Users


class UsersService(BaseService):
    model = Users
