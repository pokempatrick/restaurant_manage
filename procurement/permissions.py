from rest_framework import permissions
from helpers import constant
from procurement.models import Procurements


class IsProcuementEditable(permissions.BasePermission):
    message = "The budget is no more editable"

    def has_object_permission(self, request, view, obj):
        """
            Return `True` if permission is granted, `False` otherwise.
        """
        if (request.method in permissions.SAFE_METHODS):
            return True
        """ check if the statut for budget is editable for budget entity """
        if (isinstance(obj, Procurements)):
            return obj.statut in constant.EDITABLE_STATUT
