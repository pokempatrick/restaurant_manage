from rest_framework import permissions
from helpers import constant
from budgets.models import Budgets, DishBudgets


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
