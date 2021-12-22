from rest_framework import serializers

from src.favorites.models import Favorites
from src.music.api.serializers import AlbumListSerializer, TrackListSerializer


class FavoriteAlbumsSerializer(serializers.ModelSerializer):
    favorite_albums = AlbumListSerializer(many=True, read_only=True)

    class Meta:
        model = Favorites
        fields = "favorite_albums",


class FavoriteTracksSerializer(serializers.ModelSerializer):
    favorite_tracks = TrackListSerializer(many=True, read_only=True)

    class Meta:
        model = Favorites
        fields = "favorite_tracks",
