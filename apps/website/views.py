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
from .permissions import *
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication


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
        if self.action == 'get_all_menu_items':
            return []
        else:
            return super().get_authenticators()

    def get_permissions(self):
        """
      Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'get_all_menu_items':
            permission_classes = [AllowAny]
        else:
            permission_classes = [ISMANAGERONLY]
        return [permission() for permission in permission_classes]

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
