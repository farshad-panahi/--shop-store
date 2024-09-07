"""
AUTHENTICATION, PROFILE MANAGEMENT
"""

from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

from .manager import BaseUserManager


class BaseUser(AbstractUser):
    username = None
    first_name = models.CharField(max_length=50, blank=True, default="")
    last_name = models.CharField(max_length=50, blank=True, default="")
    email = models.EmailField(max_length=100, unique=True, db_index=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = BaseUserManager()


class Customer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, db_index=True
    )

    phone = models.CharField(max_length=11, null=True, blank=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Address(models.Model):
    customer = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        db_index=True,
    )

    province = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=255)

    def __str__(self):
        return self.province

    class Meta:
        db_table = "customer_address"
