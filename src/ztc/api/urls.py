from django.conf.urls import include, url

from rest_framework_nested import routers

from .schema import OpenAPISchemaView
from .views import (
    BesluitTypeViewSet, CatalogusViewSet, InformatieObjectTypeViewSet
)

root_router = routers.SimpleRouter()
root_router.register(r'catalogussen', CatalogusViewSet)

catalogus_router = routers.NestedSimpleRouter(root_router, r'catalogussen', lookup='catalogus')
catalogus_router.register(r'besluittypen', BesluitTypeViewSet)
catalogus_router.register(r'informatieobjecttypen', InformatieObjectTypeViewSet)


API_PREFIX = r'^v(?P<version>\d+)'


urlpatterns = [
    url('{}/schema/'.format(API_PREFIX), OpenAPISchemaView.as_view(), name='api_schema'),
    url('{}/'.format(API_PREFIX), include(root_router.urls)),
    url('{}/'.format(API_PREFIX), include(catalogus_router.urls)),
]
