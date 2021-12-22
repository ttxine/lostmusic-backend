from rest_framework import permissions


class IsNotSubscriber(permissions.BasePermission):
    """Только для неподписанных"""
    def has_permission(self, request, view):
        return not view.get_queryset().filter(user_id=view.kwargs['id']).exists()


class IsSubscriber(permissions.BasePermission):
    """Только для подписчиков"""
    def has_permission(self, request, view):
        return view.get_queryset().filter(user_id=view.kwargs['id']).exists()
