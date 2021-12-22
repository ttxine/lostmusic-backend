from django.urls import path
from django.contrib.auth import get_user_model

from rest_framework.routers import DefaultRouter

from src.oauth.api import views

urlpatterns = [
    path("users/<int:subscriber_id>/following", views.FollowingView.as_view()),
    path("users/<int:user_id>/followers", views.FollowerView.as_view())
]


router = DefaultRouter()
router.register("users", views.CustomUserViewSet)

User = get_user_model()

urlpatterns += router.urls
