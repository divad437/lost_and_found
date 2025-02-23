from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from users.managers import CustomUserManager


class User(AbstractUser):
    username = None
    first_name = models.CharField(_("first name"), max_length=50)
    last_name = models.CharField(_("last name"), max_length=50)
    phone_number = PhoneNumberField(
        _("phone number"),
        unique=True,
        blank=True,
        null=True,
    )
    email = models.EmailField(_("email address"), unique=True)
    location = models.ForeignKey(
        "City",
        verbose_name=_("city"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number", "first_name", "last_name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        db_table = "users"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class City(models.Model):
    name = models.CharField(_("city name"), max_length=50)
    slug = models.SlugField(_("slug"), max_length=50, blank=True)

    class Meta:
        verbose_name = _("city")
        verbose_name_plural = _("cities")
        db_table = "cities"

    def __str__(self):
        return self.name
