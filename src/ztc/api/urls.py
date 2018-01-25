from django.conf.urls import include, url

from rest_framework_nested import routers

from .besluittype.views import BesluitTypeViewSet
from .catalogus.views import CatalogusViewSet
from .schema import OpenAPISchemaView

root_router = routers.SimpleRouter()
root_router.register(r'catalogussen', CatalogusViewSet)

catalogus_router = routers.NestedSimpleRouter(root_router, r'catalogussen', lookup='catalogus')
catalogus_router.register(r'besluittypen', BesluitTypeViewSet)

API_PREFIX = r'^v(?P<version>\d+)'


urlpatterns = [
    url('{}/schema/'.format(API_PREFIX), OpenAPISchemaView.as_view(), name='api_schema'),
    url('{}/'.format(API_PREFIX), include(root_router.urls)),
    url('{}/'.format(API_PREFIX), include(catalogus_router.urls)),
]
