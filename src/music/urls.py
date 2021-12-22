from django.urls import path

from src.music.api import views

urlpatterns = [
    path("artists/", views.ArtistViewSet.as_view({'get': 'list'})),
    path("artists/<int:pk>", views.ArtistViewSet.as_view({'get': 'retrieve'})),
    path("genre/", views.GenreView.as_view()),
    path("albums/", views.AlbumViewSet.as_view({'get': 'list', 'post': 'create'})),
    path("albums/<int:pk>", views.AlbumViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
    path("albums/<int:pk>/add-to-favorites", views.AlbumViewSet.as_view({'post': 'add_to_favorites'})),
    path("albums/<int:pk>/remove-from-favorites", views.AlbumViewSet.as_view({'post': 'remove_from_favorites'})),
    path("albums/<int:album_id>/tracks/", views.TrackViewSet.as_view({'get': 'list', 'post': 'create'})),
    path(
        "albums/<int:album_id>/tracks/<int:pk>",
        views.TrackViewSet.as_view({
            'get':
            'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        })
    ),
    path(
        "albums/<int:album_id>/tracks/<int:pk>/add-to-favorites",
        views.TrackViewSet.as_view({'post': 'add_to_favorites'})
    ),
    path(
        "albums/<int:album_id>/tracks/<int:pk>/remove-from-favorites",
        views.TrackViewSet.as_view({'post': 'remove_from_favorites'})
    ),
]
