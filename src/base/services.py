from datetime import timedelta

from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone

from mutagen.mp3 import MP3


def validate_file_size(file):
    """Проверка на превышение максимально допустимого размера файла"""
    megabytes_limit = settings.FILE_SIZE_LIMIT * 1024 * 1024
    if file.size > megabytes_limit:
        raise ValidationError("Файл превышает максимально допустимый размер (8 MB)")


def get_avatar_upload_path(instance, file) -> str:
    """Получение пути загрузки аватара"""
    return f"img/avatar/{instance.id}/{file}"


def get_cover_upload_path(instance, file) -> str:
    """Получение пути загрузки аватара"""
    current_time = timezone.now()
    return f"img/cover/{''.join(filter(str.isdigit, str(current_time.ctime())))}/{instance}/{file}"


def get_track_upload_path(instance, file) -> str:
    """Получение пути загрузки файла трека"""
    current_time = timezone.now()
    return f"audio/tracks/{''.join(filter(str.isdigit, str(current_time.ctime())))}/{instance}/{file}"


class TrackService:

    __slots__ = 'request',

    def __init__(self, request) -> None:
        self.request = request

    def create(self, serializer, album_id):
        duration = timedelta(seconds=MP3(self.request.FILES.get('file')).info.length)
        serializer.save(album_id=album_id, duration=duration)

    def update(self, serializer):
        if self.request.FILES.get('file'):
            duration = timedelta(seconds=MP3(self.request.FILES.get('file')).info.length)
            serializer.save(duration=duration)
        else:
            return serializer.save()


class AlbumService:

    __slots__ = 'request',

    def __init__(self, request) -> None:
        self.request = request
    
    def create(self, serializer):
        cover = self.request.FILES.get('cover')
        serializer.save(release_date=timezone.now(), cover_small=cover, cover_large=cover)
    
    def update(self, serializer):
        if serializer.context.get('request').FILES.get('cover'):
            cover = self.request.FILES.get('cover')
            serializer.save(release_date=timezone.now(), cover_small=cover, cover_large=cover)
        else:
            return serializer.save()
