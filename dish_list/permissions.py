from rest_framework import permissions
from helpers import constant
from dish_list.models import DishListResult, DishResult


class IsDishResultEditable(permissions.BasePermission):
    message = "The dish result  is no more editable"

    def has_object_permission(self, request, view, obj):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        if (request.method in permissions.SAFE_METHODS):
            return True
        """ check if the statut for dishresult is editable for dishresult entity """
        if (isinstance(obj, DishResult)):
            return obj.statut in constant.EDITABLE_STATUT

        """ check if the statut for dishresult is editable for dishlistresult entity """
        if (isinstance(obj, DishListResult)):
            return obj.dish_result.statut in constant.EDITABLE_STATUT
