from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

from django_resized import ResizedImageField

from src.base.services import validate_file_size, get_cover_upload_path, get_track_upload_path

User = get_user_model()


class Album(models.Model):
    title = models.CharField("Название альбома", max_length=100)
    genre = models.ForeignKey(to="Genre", on_delete=models.CASCADE, verbose_name="Жанр")
    artists = models.ManyToManyField(to=User, related_name="albums", verbose_name="Исполнители")
    featuring = models.ManyToManyField(to=User, related_name="albums_featuring", blank=True, verbose_name="С участием")
    cover = models.ImageField(
        "Обложка",
        upload_to=get_cover_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "png"]), validate_file_size]
    )
    cover_large = ResizedImageField(
        "Обложка большая",
        size=[250, 250],
        crop=["middle", "center"],
        blank=True,
        upload_to=get_cover_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "png"]), validate_file_size]
    )
    cover_small = ResizedImageField(
        "Обложка малая",
        size=[100, 100],
        crop=["middle", "center"],
        blank=True,
        upload_to=get_cover_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "png"]), validate_file_size]
    )
    release_date = models.DateTimeField("Дата релиза")

    class AlbumType(models.TextChoices):
        ALBUM = "a", "Альбом"
        SINGLE = "s", "Сингл"

    album_type = models.CharField("Тип альбома", max_length=1, choices=AlbumType.choices)

    class Meta:
        verbose_name = "Альбом"
        verbose_name_plural = "Альбомы"

    def __str__(self) -> str:
        return self.title


class Track(models.Model):
    title = models.CharField("Название", max_length=100)
    duration = models.DurationField("Длительность")
    artists = models.ManyToManyField(to=User, related_name="tracks", verbose_name="Исполнители")
    featuring = models.ManyToManyField(to=User, related_name="tracks_featuring", blank=True, verbose_name="С участием")
    explicit = models.BooleanField("Explicit")
    playable = models.BooleanField("Доступен для прослушивания", default=True)
    text = models.TextField("Текст трека", blank=True)
    album = models.ForeignKey(to=Album, on_delete=models.CASCADE, related_name='tracks', verbose_name="Альбом")
    file = models.FileField(
        "Файл трека",
        upload_to=get_track_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=["mp3", "wav"]), validate_file_size]
    )

    class Meta:
        verbose_name = "Трек"
        verbose_name_plural = "Треки"

    def __str__(self) -> str:
        return self.title

    def get_duration_display(self) -> str:
        minutes = self.duration.seconds // 60
        seconds = self.duration.seconds % 60
        return f"{minutes}:{seconds}"


class Genre(models.Model):
    title = models.CharField("Название жанра", max_length=100)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self) -> str:
        return self.title
