from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def _create_user(self, phone_number, password, email=None, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not phone_number:
            msg = "The given phone_number must be set"
            raise ValueError(msg)
        if email:
            email = self.normalize_email(email)
        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", False)
        return self._create_user(phone_number, password, email, **extra_fields)

    def create_superuser(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            msg = "Superuser must have is_staff=True."
            raise ValueError(msg)
        if extra_fields.get("is_superuser") is not True:
            msg = "Superuser must have is_superuser=True."
            raise ValueError(msg)

        return self._create_user(phone_number, password, email, **extra_fields)
