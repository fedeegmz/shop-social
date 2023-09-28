# models
from models.user import BaseUser, User


def assert_equal_user(user_1: User, user_2: User):
    assert user_1.id == user_2.id
    assert user_1.username == user_2.username
    assert user_1.name == user_2.name
    assert user_1.lastname == user_2.lastname
    assert user_1.disabled == user_2.disabled
    assert user_1.created == user_2.created
    assert user_1.is_superuser == user_2.is_superuser

def assert_equal_base_user(user_1: BaseUser, user_2: BaseUser):
    assert user_1.id == user_2.id
    assert user_1.username == user_2.username
    assert user_1.name == user_2.name
    assert user_1.lastname == user_2.lastname