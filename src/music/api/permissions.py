from django.contrib.auth import get_user_model
from rest_framework import permissions

from src.music.models import Album

User = get_user_model()


class IsAuthorOrReadOnly(permissions.BasePermission):
    """POST, PUT, UPDATE только для автора"""
    def has_object_permission(self, request, view, obj):
        if not request.method in permissions.SAFE_METHODS:
            return request.user in obj.artists.all()
        return True


class IsParentAuthorOrReadOnly(permissions.BasePermission):
    """POST, PUT, UPDATE только для автора родителя"""
    def has_permission(self, request, view):
        album = Album.objects.get(id=view.kwargs['album_id'])
        if not request.method in permissions.SAFE_METHODS:
            return request.user in album.artists.all()
        return True


class IsFavorite(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj in request.user.favorites.favorite_albums.all() or \
            obj in request.user.favorites.favorite_tracks.all()


class IsUserExists(permissions.BasePermission):

    def has_permission(self, request, view):
        user_id = view.kwargs['user_id']
        return User.objects.filter(pk=user_id).exists()
