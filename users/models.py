from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from django.utils import timezone


from .managers import UserManager


class BaseUser(PermissionsMixin,
               AbstractBaseUser):
    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def get_full_name(self):
        return self.profile.full_name

    def get_short_name(self):
        return self.get_full_name()

    def get_description(self):
        return self.profile.description

    @property
    def name(self):
        return self.get_full_name()

    def __str__(self):
        return f'{self.email}'
