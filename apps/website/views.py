from rest_framework.response import Response
from apps.website.models import *
from apps.website.serializers import *
from rest_framework import generics, mixins, permissions, status, views, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from drf_yasg.utils import swagger_auto_schema
from apps.website.permissions import *

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
