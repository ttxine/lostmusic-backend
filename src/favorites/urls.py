from django.urls import path

from src.favorites.api.views import FavoritesView

urlpatterns = [
    path("users/<int:user_id>/favorite-albums/", FavoritesView.as_view({'get': 'albums'})),
    path("users/<int:user_id>/favorite-tracks/", FavoritesView.as_view({'get': 'tracks'})),
]