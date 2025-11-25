from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.auth.get("role") == "admin"

class IsAdminOrClient(BasePermission):
    def has_permission(self, request, view):
        return request.auth.get("role") == "admin" or request.auth.get("role") == "client"

class IsClient(BasePermission):
    def has_permission(self, request, view):
        return request.auth.get("role") == "client"

class IsAdminOrClientOrGuest(BasePermission):
    def has_permission(self, request, view):
        return request.auth.get("role") == "admin" or request.auth.get("role") == "client" or request.auth.get("role") == "guest"
