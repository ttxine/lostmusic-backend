from django_filters import rest_framework as filters

from src.music.models import Album
from src.base.selectors import get_albums


# class CharFilterInFilter(filters.BaseInFilter, filters.Char)


class AlbumFilter(filters.FilterSet):
    genre = filters.CharFilter(field_name='genre__title')

    class Meta:
        model = Album
        fields = "genre",
