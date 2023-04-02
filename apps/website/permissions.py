from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group
from rest_framework import permissions


def is_in_group(user, group_name):
    """
    Takes a user and a group name, and returns `True` if the user is in that group.
    """
    try:
        return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()
    except Group.DoesNotExist:
        return None


class ISDELIVERYCREWORCUSTOMER(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    SAFE_METHODS = ["GET", "HEAD", "OPTIONS"]

    def has_permission(self, request, view) -> bool:
        token_json = request.META.get('HTTP_AUTHORIZATION', '')
        token = token_json.split(' ')[1]
        if token:
            user = Token.objects.get(key=token)
            if request.method in self.SAFE_METHODS and is_in_group(
                    user.user, 'Delivery crew') or user.user.groups.count() == 0:
                return True
            else:
                return False
        else:
            return False


class ISDELIVERYCREW(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    SAFE_METHODS = ["GET", "HEAD", "OPTIONS", "POST"]

    def has_permission(self, request, view) -> bool:
        token_json = request.META.get('HTTP_AUTHORIZATION', '')
        token = token_json.split(' ')[1]
        if token:
            user = Token.objects.get(key=token)
            return (
                request.method in self.SAFE_METHODS and is_in_group(
                    user.user, 'Delivery crew')
            )
        else:
            return False


class ISMANAGERONLY(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    SAFE_METHODS = ["GET", "POST", "PUT",
                    "PATCH", "DELETE",  "HEAD", "OPTIONS"]

    def has_permission(self, request, view) -> bool:
        token_json = request.META.get('HTTP_AUTHORIZATION', '')
        token = token_json.split(' ')[1]
        if token:
            user = Token.objects.get(key=token)
            return (
                request.method in self.SAFE_METHODS and is_in_group(
                    user.user, 'Manager')
            )
        else:
            return False


class ISCUSTOMER(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    SAFE_METHODS = ["GET", "POST", "DELETE",  "HEAD", "OPTIONS"]

    def has_permission(self, request, view) -> bool:
        token_json = request.META.get('HTTP_AUTHORIZATION', '')
        token = token_json.split(' ')[1]
        if token:
            user = Token.objects.get(key=token)
            return (
                request.method in self.SAFE_METHODS and user.user.groups.count() == 0
            )
        else:
            return False