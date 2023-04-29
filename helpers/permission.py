from rest_framework import permissions


class IsAuthenficatedOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        return bool(request.user and request.user.is_authenticated)


class HasAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        if (request.method in permissions.SAFE_METHODS):
            return True

        return request.user.role_name in ["ROLE_ADMIN", "ROLE_SUPER_ADMIN", "ROLE_MANAGER"]


class HasOWNERRole(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        return request.user.role_name in ["ROLE_OWNER", "ROLE_ADMIN", "ROLE_SUPER_ADMIN", "ROLE_MANAGER"]


class IsUserOWNEROrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        if (request.method in permissions.SAFE_METHODS):
            return True
        return request.user.role_name in ["ROLE_OWNER", "ROLE_ADMIN", "ROLE_SUPER_ADMIN", "ROLE_MANAGER"]


class HasManagerRole(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        return request.user.role_name == "ROLE_MANAGER"


class IsUserManagerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        if (request.method in permissions.SAFE_METHODS):
            return True
        return request.user.role_name == "ROLE_MANAGER"


class HasAccoutantRole(permissions.BasePermission):
    def has_permission(self, request, view):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        return request.user.role_name == "ROLE_ACCOUNTANT"


class IsUserAccountantOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        if (request.method in permissions.SAFE_METHODS):
            return True
        return request.user.role_name == "ROLE_ACCOUNTANT"


class HasCookerRole(permissions.BasePermission):
    def has_permission(self, request, view):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        return request.user.role_name == "ROLE_COOKER"


class IsUserCookerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        if (request.method in permissions.SAFE_METHODS):
            return True
        return request.user.role_name == "ROLE_COOKER"


class HasTechnicianRole(permissions.BasePermission):
    def has_permission(self, request, view):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        return request.user.role_name == "ROLE_TECHNICIAN"


class IsUserTechnicianOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        if (request.method in permissions.SAFE_METHODS):
            return True
        return request.user.role_name == "ROLE_TECHNICIAN"


class IsUserOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        if (request.method in permissions.SAFE_METHODS):
            return True
        return request.user == obj.added_by


class IsUserOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        if (request.method in permissions.SAFE_METHODS):
            return True
        return request.user == obj
