import os
import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

from .managers import CustomUserManager


def get_avatar_filename(instance, filename):
    return f"user/{instance.username}/avatar/{filename}"
    
class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(_("email address"), unique=True)
    password = models.CharField(
        validators=[
            RegexValidator(
                regex=r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*\W)(?!.* ).{8,}$',
                message="At least 8 characters long, Contains at least one uppercase letter, lowercase letter, one digit, one special character (e.g., @, #, $, etc.)",
                code="invalid_registration",
            ),
        ],
    )

    avatar = models.ImageField(upload_to=get_avatar_filename, blank=True, null=True)
    bio = models.CharField(max_length=200, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email
'''
    def avatar(self):
        if self.avatar:
            return settings.WEBSITE_URL + self.avatar.url
        else:
            return 'https://picsum.photos/200/200'
'''

