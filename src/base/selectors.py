from django.contrib.auth import get_user_model

from src.music.models import Track, Album, Genre
from src.favorites.models import Favorites
from src.oauth.models import Follower

User = get_user_model()


def get_artists():
    return User.objects.filter(tracks__isnull=False)


def get_albums():
    return Album.objects.all()


def get_genres():
    return Genre.objects.all()


def get_or_create_favorites(user_id=None):
    if user_id:
        return Favorites.objects.get_or_create(user_id=user_id)[0]
    return Favorites.objects.none()


def get_tracks_by_album_id(album_id=None):
    if album_id:
        return Track.objects.filter(album_id=album_id)
    return Track.objects.none()


def get_followers(user_id=None):
    if user_id:
        return Follower.objects.filter(user_id=user_id)
    return Follower.objects.none()


def get_following(subscriber_id=None):
    if subscriber_id:
        return Follower.objects.filter(subscriber_id=subscriber_id)
    return Follower.objects.none()


def get_follower(user_id, subscriber_id):
    return Follower.objects.get(user_id=user_id, subscriber_id=subscriber_id)


def create_follower(user_id, subscriber_id):
    return Follower.objects.create(user_id=user_id, subscriber_id=subscriber_id)
