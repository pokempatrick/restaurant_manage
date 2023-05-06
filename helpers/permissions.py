from rest_framework import permissions
from helpers import constant
from budgets.models import Budgets, DishBudgets


class IsAuthenficatedOnly(permissions.BasePermission):
    message = "Only authenticated can perform this action"

    def has_permission(self, request, view):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        return bool(request.user and request.user.is_authenticated)


class HasAdminRole(permissions.BasePermission):
    message = "Only admin can perform this action"

    def has_permission(self, request, view):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        if (request.method in permissions.SAFE_METHODS):
            return True

        return request.user.role_name in constant.ROLE_ADMIN_HERITED


class HasOWNERRole(permissions.BasePermission):
    message = "Only owner can perform this action"

    def has_object_permission(self, request, view, obj):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        return request.user.role_name in constant.ROLE_OWNER_HERITED


class IsUserOWNEROrReadOnly(permissions.BasePermission):
    message = "Only owner can perform this action"

    def has_permission(self, request, view):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        if (request.method in permissions.SAFE_METHODS):
            return True
        return request.user.role_name in constant.ROLE_OWNER_HERITED


class HasManagerRole(permissions.BasePermission):
    message = "Only manager can perform this action"

    def has_object_permission(self, request, view, obj):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        return request.user.role_name == "ROLE_MANAGER"


class IsUserManagerOrReadOnly(permissions.BasePermission):
    message = "Only manager can perform this action"

    def has_permission(self, request, view):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        if (request.method in permissions.SAFE_METHODS):
            return True
        return request.user.role_name == "ROLE_MANAGER"


class HasAccoutantRole(permissions.BasePermission):
    message = "Only accountant can perform this action"

    def has_permission(self, request, view):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        return request.user.role_name == "ROLE_ACCOUNTANT"


class IsUserAccountantOrReadOnly(permissions.BasePermission):
    message = "Only accountant can perform this action"

    def has_permission(self, request, view):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        if (request.method in permissions.SAFE_METHODS):
            return True
        return request.user.role_name == "ROLE_ACCOUNTANT"


class HasCookerRole(permissions.BasePermission):
    message = "Only cooker can perform this action"

    def has_object_permission(self, request, view, obj):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        return request.user.role_name == "ROLE_COOKER"


class IsUserCookerOrReadOnly(permissions.BasePermission):
    message = "Only cooker can perform this action"

    def has_permission(self, request, view):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        if (request.method in permissions.SAFE_METHODS):
            return True
        return request.user.role_name == "ROLE_COOKER"


class HasTechnicianRole(permissions.BasePermission):
    message = "Only technician can perform this action"

    def has_permission(self, request, view):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        return request.user.role_name in constant.ROLE_TECHNICIAN_HERITED


class IsUserTechnicianOrReadOnly(permissions.BasePermission):
    message = "Only technician can perform this action"

    def has_permission(self, request, view):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        if (request.method in permissions.SAFE_METHODS):
            return True
        return request.user.role_name in constant.ROLE_TECHNICIAN_HERITED


class IsUserOwnerOrReadOnly(permissions.BasePermission):
    message = "Only the owner can perform this action"

    def has_object_permission(self, request, view, obj):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        if (request.method in permissions.SAFE_METHODS):
            return True
        return request.user == obj.added_by


class IsUserOwner(permissions.BasePermission):
    message = "Only the owner can perform this action"

    def has_object_permission(self, request, view, obj):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        if (request.method in permissions.SAFE_METHODS):
            return True
        return request.user == obj


class IsBudgetEditable(permissions.BasePermission):
    message = "The budget is no more editable"

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
