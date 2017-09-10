from rest_framework.exceptions import ValidationError

from .models import BaseUser


def create_user(*, email: str, password: str) -> BaseUser:
    return BaseUser.objects.create(email=email, password=password)
