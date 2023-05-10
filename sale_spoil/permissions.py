from rest_framework import permissions
from sale_spoil import constant
from datetime import timedelta
from django.utils import timezone
from sale_spoil.models import Sale, SpoilDish, SpoilIngredient


class IsAccountable(permissions.BasePermission):
    message = "Only managers can achieved this task"

    def has_permission(self, request, view):
        """
            Return `True` if permission is granted, `False` otherwise.
        """

        return request.user.role_name in constant.ACCOUNTABLE_HERITED


class IsEditable(permissions.BasePermission):
    message = "The item is no more editable. It remains editable 7 days only."

    def has_object_permission(self, request, view, obj):
        """
            Return `True` if permission is granted, `False` otherwise.
        """

        return obj.created_at + timedelta(days=7) > timezone.now()
