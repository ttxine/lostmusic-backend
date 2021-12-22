from rest_framework import generics, parsers,permissions
from rest_framework.decorators import action
from rest_framework.views import Response, status

from djoser.views import UserViewSet

from src.oauth.api.serializers import FollowerSerializer, FollowingSerializer
from src.oauth.api.permissions import IsNotSubscriber, IsSubscriber
from src.base.selectors import create_follower, get_follower, get_followers, get_following


class CustomUserViewSet(UserViewSet):
    """Доопределение viewset'а пользователя с реализацией подписки/отписки на пользователя"""

    def initialize_request(self, request, *args, **kwargs):
        self.action = self.action_map.get(request.method.lower())
        return super().initialize_request(request, *args, **kwargs)

    def get_parsers(self):
        if self.action == 'me':
           return (parsers.MultiPartParser(),)
        return super().get_parsers()
    
    def get_queryset(self):
        if self.action in ['follow', 'unfollow']:
            return get_following(subscriber_id=self.request.user.id)
        return super().get_queryset()

    @action(['post'], detail=True, permission_classes=[IsNotSubscriber], serializer_class=FollowingSerializer)
    def follow(self, request, *args, **kwargs):
        """Подписка"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = self.kwargs['id']
        sub_id = request.user.id
        create_follower(user_id=user_id, subscriber_id=sub_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(['post'], detail=True, permission_classes=[IsSubscriber], serializer_class=FollowingSerializer)
    def unfollow(self, request, *args, **kwargs):
        """Отписка"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = self.kwargs['id']
        subscriber_id = request.user.id
        obj = get_follower(user_id, subscriber_id)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowingView(generics.ListAPIView):
    """Список подписок пользователя"""
    serializer_class = FollowingSerializer
    lookup_field = 'subscriber_id'

    def get_permissions(self):
        return (permissions.IsAuthenticatedOrReadOnly(),)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return get_following()
        return get_following(self.kwargs['subscriber_id'])


class FollowerView(generics.ListAPIView):
    """Список подписчиков пользователя"""
    serializer_class = FollowerSerializer
    lookup_field = 'user_id'

    def get_permissions(self):
        return (permissions.IsAuthenticatedOrReadOnly(),)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return get_followers()
        return get_followers(self.kwargs['user_id'])
