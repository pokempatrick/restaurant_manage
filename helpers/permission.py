from rest_framework import permissions
from helpers import constant
from budgets.models import Budgets, DishBudgets


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

        return request.user.role_name in constant.ROLE_ADMIN_HERITED


class HasOWNERRole(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        return request.user.role_name in constant.ROLE_OWNER_HERITED


class IsUserOWNEROrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        if (request.method in permissions.SAFE_METHODS):
            return True
        return request.user.role_name in constant.ROLE_OWNER_HERITED


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
    def has_object_permission(self, request, view, obj):
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
        return request.user.role_name in constant.ROLE_TECHNICIAN_HERITED


class IsUserTechnicianOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        if (request.method in permissions.SAFE_METHODS):
            return True
        return request.user.role_name in constant.ROLE_TECHNICIAN_HERITED


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


class IsBudgetEditable(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        if (request.method in permissions.SAFE_METHODS):
            return True
        """ check if the statut for budget is editable for budget entity """
        if (isinstance(obj, Budgets)):
            return obj.statut in constant.EDITABLE_STATUT

        """ check if the statut for budget is editable for dishbudget entity """
        if (isinstance(obj, DishBudgets)):
            return obj.budget.statut in constant.EDITABLE_STATUT
