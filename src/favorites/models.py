from django.db import models
from django.contrib.auth import get_user_model

from src.music.models import Track, Album

User = get_user_model()


class Favorites(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='favorites', verbose_name="Пользователь")
    favorite_tracks = models.ManyToManyField(to=Track, verbose_name="Любимые треки")
    favorite_albums = models.ManyToManyField(to=Album, verbose_name="Любимые альбомы")

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self) -> str:
        return f"Избранное пользователя {self.user}"
