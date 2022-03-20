from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager


class User(AbstractBaseUser):
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    invite_code = models.CharField(max_length=6)
    activated_code = models.CharField(null=True, blank=True,
                                      default=None, max_length=6)
    confirmation_code = models.CharField(max_length=4)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ()

    objects = UserManager()

    def __str__(self):
        return str(self.phone_number)
