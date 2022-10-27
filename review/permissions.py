from rest_framework import permissions
from rest_framework.views import Request, View


class ReviewAdmPermission(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        return request.method == "GET" or request.user.is_authenticated


class isReviewAdminOrUser(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj):
        return (
            request.method == "GET" or request.user.is_staff or request.user.is_critic
        )
