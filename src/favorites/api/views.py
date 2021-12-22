from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from src.favorites.api.serializers import FavoriteAlbumsSerializer, FavoriteTracksSerializer
from src.music.api.permissions import IsUserExists
from src.base.selectors import get_or_create_favorites
from src.base.classes import MixedSerializer


class FavoritesView(MixedSerializer,viewsets.ReadOnlyModelViewSet):
    queryset = get_or_create_favorites()
    serializer_class = FavoriteTracksSerializer
    lookup_field = 'user_id'
    permission_classes = (IsUserExists,)
    serializer_classes_by_action = {
        'albums': FavoriteAlbumsSerializer,
        'tracks': FavoriteTracksSerializer
    }

    def get_object(self):
        return get_or_create_favorites(self.kwargs['user_id'])

    @action(['get'], detail=True)
    def albums(self, request, *args, **kwargs):
        favorites = self.get_object()
        serializer = self.get_serializer(favorites)
        return Response(serializer.data)
    
    @action(['get'], detail=True)
    def tracks(self, request, *args, **kwargs):
        favorites = self.get_object()
        serializer = self.get_serializer(favorites)
        return Response(serializer.data)
