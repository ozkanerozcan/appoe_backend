from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of a post to edit or delete it,
    unless the user is a superuser.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow full access if the user is a superuser
        if request.user.is_superuser:
            return True

        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the author of the post.
        return obj.created_by == request.user
