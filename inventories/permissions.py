from rest_framework import permissions
from helpers import constant
from inventories.models import Inventories


class IsInventoriesEditable(permissions.BasePermission):
    message = "The inventory  is no more editable"

    def has_object_permission(self, request, view, obj):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        if (request.method in permissions.SAFE_METHODS):
            return True
        """ check if the statut for dishresult is editable for dishresult entity """
        if (isinstance(obj, Inventories)):
            return obj.statut in constant.EDITABLE_STATUT
