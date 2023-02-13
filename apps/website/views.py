from rest_framework.response import Response
from apps.website.models import *
from apps.website.serializers import *
from rest_framework import generics, mixins, permissions, status, views, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from drf_yasg.utils import swagger_auto_schema
from apps.website.permissions import *
#


class ManagerUserGroupManagement(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    queryset = User.objects.all()
    serializer_class = UserManagementSerializer

    def get_permissions(self):
        """
      Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'create' or self.action == 'destroy':
            permission_classes = [ISMANAGERONLY]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

    @swagger_auto_schema(security=[], responses={200: UserManagementSerializer})
    def list(self, request):
        queryset = User.objects.filter(groups__name='Manager')
        serializer = UserManagementSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(security=[], responses={201: UserManagementSerializer})
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(security=[], responses={204: UserManagementSerializer})
    def destroy(self, request, *args, **kwargs):
        from .utils import perform_destory_from_user_group
        instance = self.get_object()
        destroy_status = perform_destory_from_user_group(
            group_name='Manager', user=instance)
        if destroy_status:
            return Response({'message': 'User have been removed from Group'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'No User with that id found'}, status=status.HTTP_404_NOT_FOUND)


class DeliveryCrewUserGroupManagement(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    queryset = User.objects.all()
    serializer_class = UserManagementSerializer

    def get_permissions(self):
        """
      Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'create' or self.action == 'destroy':
            permission_classes = [ISMANAGERONLY]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

    @swagger_auto_schema(security=[], responses={200: UserManagementSerializer})
    def list(self, request):
        queryset = User.objects.filter(groups__name='Delivery Crew')
        serializer = UserManagementSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(security=[], responses={201: UserManagementSerializer})
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(security=[], responses={204: UserManagementSerializer})
    def destroy(self, request, *args, **kwargs):
        from .utils import perform_destory_from_user_group
        instance = self.get_object()
        destroy_status = perform_destory_from_user_group(
            group_name='Delivery Crew', user=instance)
        if destroy_status:
            return Response({'message': 'User have been removed from Group'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'No User with that id found'}, status=status.HTTP_404_NOT_FOUND)

# READ ONLY FOR LIST and RETREIVE


class ListViewSetMenuItem(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        """
      Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [ISMANAGERONLY]
        return [permission() for permission in permission_classes]

    @swagger_auto_schema(security=[], responses={200: MenuItemSerializer})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(security=[], responses={201: MenuItemSerializer})
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(security=[], responses={200: MenuItemSerializer})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(security=[], responses={200: MenuItemSerializer})
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(security=[], responses={200: MenuItemSerializer})
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    # class ItemsView(generics.ListCreateAPIView):

    #     queryset = Items.objects.all()
    #     serializer_class = ItemSerializer
    #     ordering_fields = ['name', 'category']
    #     filterset_fields = ['name', 'category']
    #     search_fields = ['category']

    # class ItemView(generics.RetrieveUpdateDestroyAPIView):
    #     queryset = Items.objects.all()
    #     serializer_class = ItemSerializer
