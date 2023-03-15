from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the authoe of the post.
        return obj.author == request.user


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit/read it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsSafeMethod(permissions.BasePermission):
    """
    Allow access only to safe methods (GET, HEAD, OPTIONS).
    """

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
