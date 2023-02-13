from django.urls import path, include
from django.urls import path
from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework import routers
from apps.website.views import *


class OpenAPIHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = (
            ["http"] if request.get_host().startswith(
                "localhost") else ["https", "http"]
        )
        return schema


router = routers.SimpleRouter()
routes = [
    ("menu-items", ListViewSetMenuItem),
    ("groups/manager/users", ManagerUserGroupManagement, 'manager-manage'),
    ("groups/delivery-crew/users",
     DeliveryCrewUserGroupManagement, 'delivery-crew-manage'),

]

for route in routes:
    route_name = route[0]
    viewset = route[1]
    basename = route[2] if len(route) > 2 else route[0]
    router.register(route_name, viewset, basename=basename)

urlpatterns = router.urls + [
    path("", include("djoser.urls")),
    path("", include("djoser.urls.authtoken")),
]
