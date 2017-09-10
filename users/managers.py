from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def __create_user(self,
                      email,
                      password=None,
                      is_staff=False,
                      is_active=False,
                      is_superuser=False):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff,
                          is_active=is_active,
                          is_superuser=is_superuser)

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)

        return user

    def create_user(self, email, password):
        return self.__create_user(email,
                                  password,
                                  is_staff=False,
                                  is_active=False,
                                  is_superuser=False)

    def create_superuser(self, email, password):
        return self.__create_user(email,
                                  password,
                                  is_staff=True,
                                  is_active=True,
                                  is_superuser=True)

    def create(self, **kwargs):
        """
        Important to have this to get factories working by default
        """
        return self.create_user(**kwargs)
