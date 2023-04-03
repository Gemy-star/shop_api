from apps.website.views import *
from django.urls import path, include
from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework import routers


class OpenAPIHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = (
            ["http"] if request.get_host().startswith(
                "127.0.0.1") else ["https", "http"]
        )
        return schema


menu_items = MenuItemViewset.as_view({
    'get': 'get_all_menu_items',
    'post': 'post_menu_item'
})

menu_items_pk = MenuItemViewset.as_view({
    'put': 'put_menu_item',
    'delete': 'delete_menu_item',
    'get':'get_single_menu_items'
})
cart_items = CartMenuItemsViewSet.as_view({
    'get': 'get_all_menu_items',
    'delete': 'delete_items_from_cart',
    'post':'add_item_to_cart'
})
orders = OrderViewSet.as_view({
    'get': 'get_all_orders',
    'post': 'post_order'
})
orders_pk = OrderViewSet.as_view({
    'delete': 'delete_order',
    'put':'put_order'
})
manager_users = ManagerGroupViewSet.as_view({
    'get': 'get_all_managers',
    'post': 'add_user_to_manager'
})

manager_userspk = ManagerGroupViewSet.as_view({
    'delete': 'delete_user_from_manager',
})
delivery_crew_users = DeliveryCrewGroupViewSet.as_view({
    'get': 'get_all_delivery_crew',
    'post': 'add_user_to_delivery_crew'
})

delivery_crew_userspk = DeliveryCrewGroupViewSet.as_view({
    'delete': 'delete_user_from_delivery_crew',
})


urlpatterns = [
    path('users/users/me', user_info, name='get-token'),
    path('users', create_users, name='create-users'),
    path('token/login', api_token_auth, name='get-token'),
    path('menu-items', menu_items, name='menu-items'),
    path('menu-items/<menuItem>', menu_items_pk, name='menu-items-pk'),
    path('groups/manager/users', manager_users, name='manager-users'),
    path('groups/manager/users/<userId>', manager_userspk, name='manager-users-pk'),
    path('groups/delivery-crew/users', delivery_crew_users, name='delivery-crew-users'),
    path('groups/delivery-crew/users/<userId>', delivery_crew_userspk, name='delivery-crew-users-pk'),
    path('cart/menu-items', cart_items, name='cart-items'),
    path('orders/', orders, name='orders'),
    path('orders/<orderId>', orders_pk, name='orders'),

]
