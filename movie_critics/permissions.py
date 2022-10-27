from rest_framework import permissions
from rest_framework.views import Request, View


class isAdminOrUser(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj):
        return obj.id == request.user.id or request.user.is_staff
