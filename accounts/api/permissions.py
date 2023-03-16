from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit/read it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username
