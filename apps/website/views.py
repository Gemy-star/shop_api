from rest_framework.response import Response
from apps.website.models import *
from apps.website.serializers import *
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from apps.website.permissions import *
from apps.website.utils import *
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes, action
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.website.permissions import *
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from datetime import datetime
@swagger_auto_schema(methods=['POST'], request_body=RegisterSerializer)
@api_view(["POST"])
@permission_classes((AllowAny,))
def create_users(request):
    register_serializer = RegisterSerializer(data=request.data)
    if not register_serializer.is_valid():
        return Response(register_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create_user(username=register_serializer.data['username'],
                                    email=register_serializer.data['email'],
                                    password=register_serializer.data['password'])
    if not user:
        return Response({'detail': 'Invalid Credentials or activate account'}, status=status.HTTP_404_NOT_FOUND)
    user_Serializer = UserSerializer(user)
    return Response({
        'user': user_Serializer.data,
    }, status=status.HTTP_200_OK)


@swagger_auto_schema(methods=['POST'], request_body=UserSigninSerializer)
@api_view(["POST"])
@permission_classes((AllowAny,))
def api_token_auth(request):
    signin_serializer = UserSigninSerializer(data=request.data)
    if not signin_serializer.is_valid():
        return Response(signin_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(
        username=signin_serializer.data['username'],
        password=signin_serializer.data['password']
    )
    if not user:
        return Response({'detail': 'Invalid Credentials or activate account'}, status=status.HTTP_404_NOT_FOUND)

    # TOKEN STUFF
    token, _ = Token.objects.get_or_create(user=user)

    user_serialized = UserSerializer(user)

    return Response({
        'user': user_serialized.data,
        'token': token.key
    }, status=status.HTTP_200_OK)


@swagger_auto_schema(methods=['GET'])
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def user_info(request):
    user_Serializer = UserSerializer(request.user)
    if request.user:
        return Response({
            'user': user_Serializer.data,
        }, status=status.HTTP_200_OK)
    else:
        return Response(user_Serializer.errors, status=status.HTTP_403_FORBIDDEN)


class MenuItemViewset(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    authentication_classes = (TokenAuthentication,)

    def initialize_request(self, request, *args, **kwargs):
        self.action = self.action_map.get(request.method.lower())
        return super().initialize_request(request, *args, **kwargs)

    def get_authenticators(self):
        if self.action == 'get_all_menu_items' or self.action == 'get_single_menu_items':
            return []
        else:
            return super().get_authenticators()

    def get_permissions(self):
        """
      Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'get_all_menu_items' or self.action == 'get_single_menu_items':
            permission_classes = [ISDELIVERYCREWORCUSTOMER]
        else:
            permission_classes = [ISMANAGERONLY]
        return [permission() for permission in permission_classes]
    @action(detail=True, methods=['get'], url_path='menu-items/')
    def get_single_menu_items(self, request,menuItem=None):
        try:
            item = MenuItem.objects.get(pk=menuItem)
            serialized_items = MenuItemSerializer(item)
            return Response(serialized_items.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"error":f"{str(ex)}"}, status=status.HTTP_404_NOT_FOUND)
            
    @action(detail=False, methods=['get'], url_path='menu-items/')
    def get_all_menu_items(self, request):
        items = MenuItem.objects.all()
        serialized_items = MenuItemSerializer(items, many=True)
        return Response(serialized_items.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='menu-items/')
    def post_menu_item(self, request):
        item_serializer = MenuItemSerializer(data=request.data)
        if not item_serializer.is_valid():
            return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        item = MenuItem.objects.create(title=item_serializer.validated_data['title'], featured=item_serializer.validated_data['featured'], price=item_serializer.validated_data['price'],
                                       category_id=item_serializer.validated_data['category_id'])
        item_created = MenuItemSerializer(item)
        return Response(item_created.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put'], url_path='menu-items/')
    def put_menu_item(self, request,menuItem=None):
        try:
            item_serializer = MenuItemSerializer(data=request.data)
            if not item_serializer.is_valid():
               return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            item = MenuItem.objects.get(pk=menuItem)
            item.title = item_serializer.validated_data['title']
            item.featured = item_serializer.validated_data['featured']
            item.price = item_serializer.validated_data['price']
            item.category_id = item_serializer.validated_data['category_id']
            item.save()
            item_updated = MenuItemSerializer(item)
            return Response(item_updated.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"error":f"{str(ex)}"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['delete'], url_path='menu-items/')
    def delete_menu_item(self, request,menuItem=None):
        try:
            item = MenuItem.objects.get(pk=menuItem)
            item.delete()
            return Response({"message":f"item with id:{menuItem} deleted"}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"error":f"{str(ex)}"}, status=status.HTTP_404_NOT_FOUND)


class ManagerGroupViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [ISMANAGERONLY,]

    def initialize_request(self, request, *args, **kwargs):
        self.action = self.action_map.get(request.method.lower())
        return super().initialize_request(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'], url_path='groups/manager/users/')
    def get_all_managers(self, request):
        users = User.objects.filter(groups__name='Manager')
        serialized_users = UserSerializer(users, many=True)
        return Response(serialized_users.data, status=status.HTTP_200_OK)
    @action(detail=False, methods=['post'], url_path='groups/manager/users/')
    def add_user_to_manager(self,request):
        try:
            user_serializer = UserSerializer(data=request.data)
            if not user_serializer.is_valid():
               return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.get(username=user_serializer.validated_data['username'])
            managers = Group.objects.get(name='Manager') 
            managers.user_set.add(user)
            managers.save()
            user_json = UserSerializer(user)
            return Response(user_json.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"error":f"User Not Found :{str(ex)}"}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=['delete'], url_path='groups/manager/users/')
    def delete_user_from_manager(self, request,userId=None):
        try:
            user = User.objects.get(pk=userId)
            managers = Group.objects.get(name='Manager') 
            managers.user_set.remove(user)
            return Response({"message":f"User with id:{userId} deleted from Manager"}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"error":f"User Not Found {str(ex)}"}, status=status.HTTP_404_NOT_FOUND)



class DeliveryCrewGroupViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [ISMANAGERONLY,]

    def initialize_request(self, request, *args, **kwargs):
        self.action = self.action_map.get(request.method.lower())
        return super().initialize_request(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'], url_path='groups/delivery-crew/users/')
    def get_all_delivery_crew(self, request):
        users = User.objects.filter(groups__name='Delivery crew')
        serialized_users = UserSerializer(users, many=True)
        return Response(serialized_users.data, status=status.HTTP_200_OK)
    @action(detail=False, methods=['post'], url_path='groups/delivery-crew/users/')
    def add_user_to_delivery_crew(self,request):
        try:
            user_serializer = UserSerializer(data=request.data)
            if not user_serializer.is_valid():
               return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.get(username=user_serializer.validated_data['username'])
            delivery_crew = Group.objects.get(name='Delivery crew') 
            delivery_crew.user_set.add(user)
            delivery_crew.save()
            user_json = UserSerializer(user)
            return Response(user_json.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"error":f"User Not Found :{str(ex)}"}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=['delete'], url_path='groups/delivery-crew/users/')
    def delete_user_from_delivery_crew(self, request,userId=None):
        try:
            user = User.objects.get(pk=userId)
            delivery_crew = Group.objects.get(name='Delivery crew') 
            delivery_crew.user_set.remove(user)
            return Response({"message":f"User with id:{userId} deleted from delivery crew"}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"error":f"User Not Found {str(ex)}"}, status=status.HTTP_404_NOT_FOUND)


class CartMenuItemsViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all().only('menuitem').distinct()
    # queryset = Cart.objects.all()
    serializer_class = CartSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [ISCUSTOMER,]
    @action(detail=False, methods=['get'], url_path='cart/menu-items/')
    def get_all_menu_items(self, request):
        try:
            items = Cart.objects.filter(user_id = request.user.pk).only('menuitem').distinct()
            serialized_items = CartSerializer(items, many=True)
            return Response(serialized_items.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"error":f"User Not Found {str(ex)}"}, status=status.HTTP_404_NOT_FOUND)
    @action(detail=False, methods=['get'], url_path='cart/menu-items/')
    def get_all_menu_items(self, request):
        try:
            items = Cart.objects.filter(user_id = request.user.pk).only('menuitem').distinct()
            serialized_items = CartSerializer(items, many=True)
            return Response(serialized_items.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"error":f"User Not Found {str(ex)}"}, status=status.HTTP_404_NOT_FOUND)
    @action(detail=False, methods=['post'], url_path='cart/menu-items/')
    def add_item_to_cart(self,request):
        try:
            cart_serializer = CartSerializer(data=request.data)
            if not cart_serializer.is_valid():
               return Response(cart_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            menu_item = MenuItem.objects.get(pk=cart_serializer.validated_data['menu_item_id'])
            user = User.objects.get(pk=request.user.id)
            cart = Cart.objects.create(menuitem=menu_item , user=user , quantity = cart_serializer.validated_data['quantity']
                                       ,price = cart_serializer.validated_data['price'],unit_price = cart_serializer.validated_data['unit_price'])
            cart_json = CartSerializer(cart) 
            return Response(cart_json.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"error":f"Check your data :{str(ex)}"}, status=status.HTTP_404_NOT_FOUND)
    @action(detail=True, methods=['delete'], url_path='cart/menu-items/')
    def delete_items_from_cart(self, request):
        try:
            user = User.objects.get(pk=request.user.id)
            Cart.objects.filter(user=user).delete()
            return Response({"message":f"items for User with id:{user.id} deleted from cart"}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"error":f"User Not Found {str(ex)}"}, status=status.HTTP_404_NOT_FOUND)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderWithItemsSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated,]

    def initialize_request(self, request, *args, **kwargs):
        self.action = self.action_map.get(request.method.lower())
        return super().initialize_request(request, *args, **kwargs)
    @action(detail=False, methods=['get'], url_path='orders/')
    def get_all_orders(self, request):
        try:
            if not is_in_group(request.user , 'Manager') and not is_in_group(request.user , 'Delivery crew'):
                orders = Order.objects.filter(user=request.user)
                orders_serialized = OrderWithItemsSerializer(orders,many=True)
                return Response(orders_serialized.data, status=status.HTTP_200_OK)
            if is_in_group(request.user , 'Manager'):
                orders = Order.objects.all()
                orders_serialized = OrderWithItemsSerializer(orders,many=True)
                return Response(orders_serialized.data, status=status.HTTP_200_OK) 
            if is_in_group(request.user , 'Delivery crew'):
                orders = Order.objects.filter(delivery_crew=request.user)
                orders_serialized = OrderWithItemsSerializer(orders,many=True)
                return Response(orders_serialized.data, status=status.HTTP_200_OK) 
        except Exception as ex:
            return Response({"error":f"Error Happend {str(ex)}"}, status=status.HTTP_404_NOT_FOUND)
    @action(detail=False, methods=['post'], url_path='orders/')
    def post_order(self, request):
        try:
            if not is_in_group(request.user , 'Manager') and not is_in_group(request.user , 'Delivery crew'):
                cart_items = Cart.objects.filter(user=request.user)
                order = Order.objects.create(user=request.user , total = 0 ,date = datetime.now().date() )
                for item in cart_items:
                    OrderItem.objects.create(order=order ,menuitem = item.menuitem , unit_price = item.unit_price , price = item.price)
                cart_items.delete()
        except Exception as ex:
            return Response({"error":f"Error Happend {str(ex)}"}, status=status.HTTP_404_NOT_FOUND)
    @action(detail=True, methods=['delete'],url_path='orders/')
    def delete_order(self, request,orderId=None):
        try:
            if not is_in_group(request.user , 'Manager') and not is_in_group(request.user , 'Delivery crew'):
                Order.objects.get(pk=orderId).delete()
                return Response({"message":f"Order with {orderId} had been Deleted "} , status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"error":f"No Order with {orderId}{str(ex)}"}, status=status.HTTP_404_NOT_FOUND)
    @swagger_auto_schema(methods=['PUT'], request_body=DeliveryStatusSerializer)
    @action(detail=True, methods=['put'],url_path='orders/')
    def put_order(self, request,orderId=None):
        try:
            if is_in_group(request.user , 'Delivery crew'):
                status_data = DeliveryStatusSerializer(request.data)
                if not status_data.is_valid():
                    return Response(status_data.errors, status=status.HTTP_400_BAD_REQUEST)
                order = Order.objects.get(pk=orderId)
                order.status = status_data.validated_data['status']
                order.save()
                return Response({"message":f"Order with {orderId} had been Updated "} , status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"error":f"No Order with {orderId}{str(ex)}"}, status=status.HTTP_404_NOT_FOUND)