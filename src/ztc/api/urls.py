from django.conf import settings
from django.conf.urls import include, url
from django.core.exceptions import ImproperlyConfigured
from django.views.generic import RedirectView

from rest_framework_nested import routers

from .schema import schema_view
from .views import (
    BesluitTypeViewSet, CatalogusViewSet, EigenschapViewSet,
    InformatieObjectTypeViewSet, ResultaatTypeViewSet, RolTypeViewSet,
    StatusTypeViewSet, ZaakInformatieobjectTypeArchiefregimeViewSet,
    ZaakObjectTypeViewSet, ZaakTypeInformatieObjectTypeViewSet,
    ZaakTypenRelatieViewSet, ZaakTypeViewSet
)

root_router = routers.DefaultRouter()
root_router.register(r'catalogussen', CatalogusViewSet)

catalogus_router = routers.NestedSimpleRouter(root_router, r'catalogussen', lookup='catalogus')
# catalogus_router.register(r'besluittypen', BesluitTypeViewSet)
# catalogus_router.register(r'informatieobjecttypen', InformatieObjectTypeViewSet)
catalogus_router.register(r'zaaktypen', ZaakTypeViewSet)

# zaaktype_router = routers.NestedSimpleRouter(catalogus_router, r'zaaktypen', lookup='zaaktype')
# zaaktype_router.register(r'eigenschappen', EigenschapViewSet)
# zaaktype_router.register(r'resultaattypen', ResultaatTypeViewSet)
# zaaktype_router.register(r'roltypen', RolTypeViewSet)
# zaaktype_router.register(r'statustypen', StatusTypeViewSet)
# zaaktype_router.register(r'zaakobjecttypen', ZaakObjectTypeViewSet)

# zaaktype_router.register(r'heeft_gerelateerd', ZaakTypenRelatieViewSet)
# zaaktype_router.register(r'heeft_relevant', ZaakTypeInformatieObjectTypeViewSet, base_name='zktiot')
# zaaktype_router.register(r'bepaalt_afwijkend_archiefregime_van',
#                          ZaakInformatieobjectTypeArchiefregimeViewSet, base_name='rstiotarc')


API_PREFIX = r'^v(?P<version>\d+)'

DEFAULT_VERSION = settings.REST_FRAMEWORK.get('DEFAULT_VERSION')
if DEFAULT_VERSION is None:
    raise ImproperlyConfigured("Missing DEFAULT_VERSION setting in REST_FRAMEWORK configuration")


urlpatterns = [
    url(r'{}/schema(?P<format>.json|.yaml)$'.format(API_PREFIX),
        schema_view.without_ui(cache_timeout=None), name='api-schema-json'),
    url(r'{}/schema/$'.format(API_PREFIX), schema_view.with_ui('redoc', cache_timeout=None), name='api-schema'),

    url('{}/'.format(API_PREFIX), include(root_router.urls)),
    url('{}/'.format(API_PREFIX), include(catalogus_router.urls)),
    # url('{}/'.format(API_PREFIX), include(zaaktype_router.urls)),

    url('', RedirectView.as_view(url='/api/v{}/'.format(DEFAULT_VERSION))),
]
