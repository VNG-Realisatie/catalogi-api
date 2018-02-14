from django.conf.urls import include, url

from rest_framework_nested import routers

from .schema import schema_view
from .views import (
    BesluitTypeViewSet, CatalogusViewSet, EigenschapViewSet,
    InformatieObjectTypeViewSet, InformatieObjectTypeZaakTypeSerializerViewSet,
    ResultaatTypeViewSet, RolTypeViewSet, StatusTypeViewSet,
    ZaakObjectTypeViewSet, ZaakTypeInformatieObjectTypeViewSet,
    ZaakTypenRelatieViewSet, ZaakTypeViewSet
)

root_router = routers.SimpleRouter()
root_router.register(r'catalogussen', CatalogusViewSet)

catalogus_router = routers.NestedSimpleRouter(root_router, r'catalogussen', lookup='catalogus')
catalogus_router.register(r'besluittypen', BesluitTypeViewSet)
catalogus_router.register(r'informatieobjecttypen', InformatieObjectTypeViewSet)
catalogus_router.register(r'zaaktypen', ZaakTypeViewSet)
# TODO: should zaakobjecttype go nested under zaaktype??
catalogus_router.register(r'zaakobjecttypen', ZaakObjectTypeViewSet)

zaaktype_router = routers.NestedSimpleRouter(catalogus_router, r'zaaktypen', lookup='zaaktype')
zaaktype_router.register(r'eigenschappen', EigenschapViewSet)
zaaktype_router.register(r'resultaattypen', ResultaatTypeViewSet)
zaaktype_router.register(r'roltypen', RolTypeViewSet)
zaaktype_router.register(r'statustypen', StatusTypeViewSet)
zaaktype_router.register(r'heeft_gerelateerd', ZaakTypenRelatieViewSet)
zaaktype_router.register(r'heeft_relevant', ZaakTypeInformatieObjectTypeViewSet, base_name='zktiot')

iot_router = routers.NestedSimpleRouter(catalogus_router, r'informatieobjecttypen', lookup='informatieobjecttype')
iot_router.register(r'is_relevant_voor', InformatieObjectTypeZaakTypeSerializerViewSet, base_name='iotzkt')


API_PREFIX = r'^v(?P<version>\d+)'


urlpatterns = [
    url(r'{}/schema(?P<format>.json|.yaml)$'.format(API_PREFIX), schema_view.without_ui(cache_timeout=None), name='api-schema-json'),
    url(r'{}/schema/$'.format(API_PREFIX), schema_view.with_ui('redoc', cache_timeout=None), name='api-schema'),

    url('{}/'.format(API_PREFIX), include(root_router.urls)),
    url('{}/'.format(API_PREFIX), include(catalogus_router.urls)),
    url('{}/'.format(API_PREFIX), include(zaaktype_router.urls)),
    url('{}/'.format(API_PREFIX), include(iot_router.urls)),
]
