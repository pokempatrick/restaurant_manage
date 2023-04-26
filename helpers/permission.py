from rest_framework import permissions


class HasAdminRole(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        if (request.method in permissions.SAFE_METHODS):
            return True

        return request.user.role_name in ["ROLE_ADMIN", "ROLE_SUPER_ADMIN", "ROLE_MANAGER"]


class HasManagerRole(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        # if (request.method in permissions.SAFE_METHODS):
        #     return True

        return request.user.role_name == "ROLE_MANAGER"


class HasAccoutantRole(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        # if (request.method in permissions.SAFE_METHODS):
        #     return True
        return request.user.role_name == "ROLE_ACCOUNTANT"


class HasCollectorRole(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        # if (request.method in permissions.SAFE_METHODS):
        #     return True

        return request.user.role_name == "ROLE_COLLECTOR"


class HasCollectorRole(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        # if (request.method in permissions.SAFE_METHODS):
        #     return True

        return request.user.role_name == "ROLE_INSPECTOR"


class IsUserOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        if (request.method in permissions.SAFE_METHODS):
            return True
        return request.user == obj
