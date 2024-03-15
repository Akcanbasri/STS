from rest_framework import permissions


class IsStudent(permissions.BasePermission):
    """only students are allowed."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "student"


class IsTeacher(permissions.BasePermission):
    """only teachers are allowed."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "teacher"


class IsParent(permissions.BasePermission):
    """only parents are allowed."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "parent"


class IsAdministrator(permissions.BasePermission):
    """only administrators are allowed."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == "administrator" or request.user.is_superuser
        )
