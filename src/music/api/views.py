from rest_framework import viewsets, parsers, generics, permissions
from rest_framework.decorators import action
from rest_framework.views import Response, status
from django_filters import rest_framework as filters

from src.music.api.filters import AlbumFilter
from src.music.api import serializers
from src.music.api.permissions import IsAuthorOrReadOnly, IsParentAuthorOrReadOnly, IsFavorite
from src.base.classes import MixedPermissions, MixedSerializer
from src.base.services import TrackService, AlbumService
from src.base import selectors


class TrackViewSet(MixedPermissions, MixedSerializer, viewsets.ModelViewSet):
    """Вывод, изменение, удаление треков (по id альбома, которому они принадлежат)"""
    serializer_class = serializers.TrackUploadSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_classes_by_action = {
        'list': serializers.TrackListSerializer,
        'retrieve': serializers.TrackDetailSerializer,
        'add_to_favorites': serializers.FavoritesAddRemoveTrackSerializer,
        'remove_from_favorites': serializers.FavoritesAddRemoveTrackSerializer,
    }
    permission_classes_by_action = {
        'create': (IsParentAuthorOrReadOnly,),
        'update': (IsParentAuthorOrReadOnly,),
        'partial_update': (IsParentAuthorOrReadOnly,),
        'remove_from_favorites': (permissions.IsAuthenticated, IsFavorite)
    }

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return selectors.get_tracks_by_album_id()
        return selectors.get_tracks_by_album_id(self.kwargs['album_id'])

    def get_parsers(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return (parsers.MultiPartParser(),)
        return super().get_parsers()

    def perform_create(self, serializer):
        TrackService(self.request).create(serializer, self.kwargs['album_id'])

    def perform_update(self, serializer):
        TrackService(self.request).update(self, serializer)

    @action(['post'], detail=True, permission_classes=(permissions.IsAuthenticated,))
    def add_to_favorites(self, request, *args, **kwargs):
        favorites = selectors.get_or_create_favorites(user_id=request.user.id)
        favorites.favorite_tracks.add(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(['post'], detail=True)
    def remove_from_favorites(self, request, *args, **kwargs):
        favorites = selectors.get_or_create_favorites(user_id=request.user.id)
        favorites.favorite_tracks.remove(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)


class AlbumViewSet(MixedSerializer, MixedPermissions, viewsets.ModelViewSet):
    """Вывод, изменение, удаление альбомов"""
    queryset = selectors.get_albums()
    serializer_class = serializers.AlbumUploadSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_classes_by_action = {
        'list': serializers.AlbumListSerializer,
        'retrieve': serializers.AlbumDetailSerializer,
        'add_to_favorites': serializers.FavoritesAddRemoveAlbumSerializer,
        'remove_from_favorites': serializers.FavoritesAddRemoveAlbumSerializer,
    }
    permission_classes_by_action = {
        'update': (IsAuthorOrReadOnly,),
        'partial_update': (IsParentAuthorOrReadOnly,),
        'remove_from_favorites': (permissions.IsAuthenticated, IsFavorite)
    }
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AlbumFilter

    def get_parsers(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return (parsers.MultiPartParser(),)
        return super().get_parsers()

    def perform_create(self, serializer):
       AlbumService(self.request).create(serializer)

    def perform_update(self, serializer):
        AlbumService(self.request).update(serializer)

    @action(['post'], detail=True, permission_classes=(permissions.IsAuthenticated,))
    def add_to_favorites(self, request, *args, **kwargs):
        favorites = selectors.get_or_create_favorites(user_id=request.user.id)
        favorites.favorite_albums.add(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(['post'], detail=True)
    def remove_from_favorites(self, request, *args, **kwargs):
        favorites = selectors.get_or_create_favorites(user_id=request.user.id)
        favorites.favorite_albums.remove(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenreView(generics.ListAPIView):
    """Вывод жанров"""
    serializer_class = serializers.GenreSerializer
    queryset = selectors.get_genres()


class ArtistViewSet(MixedSerializer, viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.ArtistListSerializer
    serializer_classes_by_action = {
        'list': serializers.ArtistListSerializer,
        'retrieve': serializers.ArtistDetailSerializer
    }

    def get_queryset(self):
        return selectors.get_artists()
