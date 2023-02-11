from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User


class IsAuthenticatedOrReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    SAFE_METHODS = ["GET", "HEAD", "OPTIONS"]

    def has_permission(self, request, view) -> bool:
        return (
            request.method in self.SAFE_METHODS or request.user and request.user.is_authenticated
        )


class ISDELIVERYCREWORCUSTOMER(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    SAFE_METHODS = ["GET", "HEAD", "OPTIONS"]

    def has_permission(self, request, view) -> bool:
        return (
            request.method in self.SAFE_METHODS and User.objects.filter(
                pk=request.user.pk, groups__name='Delivery crew').exists() or request.user.groups.count() == 0
        )


class ISMANAGERONLY(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    SAFE_METHODS = ["GET", "POST", "PUT",
                    "PATCH", "DELETE",  "HEAD", "OPTIONS"]

    def has_permission(self, request, view) -> bool:
        return (
            request.method in self.SAFE_METHODS and User.objects.filter(
                pk=request.user.pk, groups__name='Manager').exists() and request.user.is_authenticated
        )
