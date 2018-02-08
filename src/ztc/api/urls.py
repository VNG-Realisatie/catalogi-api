from django.conf.urls import include, url

from rest_framework_nested import routers

from .schema import schema_view
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
    url(r'{}/schema(?P<format>.json|.yaml)$'.format(API_PREFIX), schema_view.without_ui(cache_timeout=None), name='api-schema-json'),
    url(r'{}/schema/$'.format(API_PREFIX), schema_view.with_ui('redoc', cache_timeout=None), name='api-schema'),

    url('{}/'.format(API_PREFIX), include(root_router.urls)),
    url('{}/'.format(API_PREFIX), include(catalogus_router.urls)),
]
