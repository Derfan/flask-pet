from werkzeug.security import safe_str_cmp
from models.user import UserModel


def authenticate(login, password):
    user = UserModel.find_by_key('login', login)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_key('id', user_id)
