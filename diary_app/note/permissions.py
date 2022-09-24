from rest_framework import permissions


class IsCorrectDiaryOrReadOnly(permissions.BasePermission):
    pass


class IsPrivateDiary(permissions.BasePermission):
    pass


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user
