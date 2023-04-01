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

urlpatterns = [
    path('users/users/me', user_info, name='get-token'),
    path('users', create_users, name='create-users'),
    path('token/login', api_token_auth, name='get-token'),
    path('menu-items', menu_items, name='menu-items'),

]
