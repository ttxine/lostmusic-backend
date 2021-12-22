from rest_framework import serializers

from src.music.models import Album, Track, Genre, User


class GenreSerializer(serializers.ModelSerializer):
    """Жанры"""

    class Meta:
        model = Genre
        fields = 'title',


class TrackListSerializer(serializers.ModelSerializer):
    """Список треков"""
    artists = serializers.SlugRelatedField("display_name", many=True, read_only=True)

    class Meta:
        model = Track
        fields = 'id', 'title', 'artists'


class TrackDetailSerializer(serializers.ModelSerializer):
    """Трек детально"""
    artists = serializers.SlugRelatedField("display_name", many=True, read_only=True)
    duration = serializers.SerializerMethodField('get_duration')

    class Meta:
        model = Track
        fields = '__all__'
    
    def get_duration(self, instance):
        return instance.get_duration_display()


class TrackUploadSerializer(serializers.ModelSerializer):
    """Загрузка трека"""

    class Meta:
        model = Track
        exclude = 'duration', 'playable', 'album'


class FavoritesAddRemoveTrackSerializer(serializers.ModelSerializer):
    """Добавление трека в избранное"""

    class Meta:
        model = Track
        fields = "id",


class AlbumListSerializer(serializers.ModelSerializer):
    """Список альбомов"""
    artists = serializers.SlugRelatedField("display_name", many=True, read_only=True)
    tracks = TrackListSerializer(many=True, read_only=True)
    genre = GenreSerializer(read_only=True)

    class Meta:
        model = Album
        fields = 'id', 'title', 'artists', 'tracks', 'genre', 'cover_large'


class AlbumDetailSerializer(serializers.ModelSerializer):
    """Альбом детально"""
    artists = serializers.SlugRelatedField("display_name", many=True, read_only=True)
    tracks = TrackDetailSerializer(many=True, read_only=True)
    genre = GenreSerializer(read_only=True)

    class Meta:
        model = Album
        fields = '__all__'


class AlbumUploadSerializer(serializers.ModelSerializer):
    """Загрузка альбома"""

    class Meta:
        model = Album
        exclude = 'release_date', 'cover_large', 'cover_small'


class FavoritesAddRemoveAlbumSerializer(serializers.ModelSerializer):
    """Добавление альбома в избранное"""

    class Meta:
        model = Album
        fields = "id",


class ArtistListSerializer(serializers.ModelSerializer):
    albums = serializers.SlugRelatedField("title", many=True, read_only=True)
    tracks = serializers.SlugRelatedField("title", many=True, read_only=True)

    class Meta:
        model = User
        fields = 'id', 'display_name', 'albums', 'tracks'


class ArtistDetailSerializer(serializers.ModelSerializer):
    albums = AlbumListSerializer(many=True, read_only=True)
    tracks = TrackListSerializer(many=True, read_only=True)
    followers_count = serializers.SerializerMethodField('get_followers_count')

    class Meta:
        model = User
        fields = 'id', 'display_name', 'albums', 'tracks', 'followers_count'

    def get_followers_count(self, instance):
        return instance.followers.count()
