from rest_framework import permissions


class CustomObjectPermissions(permissions.DjangoObjectPermissions):
    """
    Similar to `DjangoObjectPermissions`, but adding 'view' permissions.
    """
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
        'HEAD': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class ManagerFullAccess(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.user_type == "MANAGER" and obj.owner == request.user

    def has_permission(self, request, view):
        return request.user.user_type == "MANAGER"


class DeveloperFullAccess(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.user_type == "DEVELOPER" and obj.owner == request.user

    def has_permission(self, request, view):
        return request.user.user_type == "DEVELOPER"


class PermsForVacation(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.user.user_type == "DEVELOPER" and obj.owner == request.user) or \
                (request.user.user_type == "MANAGER")

    def has_permission(self, request, view):
        return request.user.user_type == "DEVELOPER" or request.user.user_type == "MANAGER"
