from django.db import models
from django.core import validators
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from src.base.services import get_avatar_upload_path, validate_file_size
from src.oauth.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("Email", max_length=255, validators=[validators.validate_email], unique=True)
    display_name = models.CharField("Отображаемое имя", max_length=100, blank=True, null=True)
    about = models.TextField("О пользователе", max_length=2500, blank=True, null=True)
    avatar = models.ImageField(
        "Аватар",
        upload_to=get_avatar_upload_path,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png']), validate_file_size]
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


class Follower(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='followers', verbose_name="Пользователь")
    subscriber = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name="Подписчик")

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'

    def __str__(self):
        return f"{self.subscriber} подписался на {self.user}"
