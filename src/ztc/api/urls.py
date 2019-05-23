from django.conf.urls import url
from django.urls import include, path

from vng_api_common import routers
from vng_api_common.schema import SchemaView

from .views import (
    BesluitTypeViewSet, CatalogusViewSet, EigenschapViewSet,
    InformatieObjectTypeViewSet, ResultaatTypeViewSet, RolTypeViewSet,
    StatusTypeViewSet, ZaakTypeInformatieObjectTypeViewSet, ZaakTypeViewSet
)

router = routers.DefaultRouter()
router.register(r'catalogussen', CatalogusViewSet, [
    routers.nested('zaaktypen', ZaakTypeViewSet, [
        routers.nested('statustypen', StatusTypeViewSet),
        routers.nested('eigenschappen', EigenschapViewSet),
        routers.nested('roltypen', RolTypeViewSet),
    ]),
    routers.nested('informatieobjecttypen', InformatieObjectTypeViewSet),
    routers.nested('besluittypen', BesluitTypeViewSet),
])
router.register(r'resultaattypen', ResultaatTypeViewSet),
router.register(r'zaaktype-informatieobjecttypen', ZaakTypeInformatieObjectTypeViewSet)


urlpatterns = [
    url(r'^v(?P<version>\d+)/', include([

        # API documentation
        url(r'^schema/openapi(?P<format>\.json|\.yaml)$',
            SchemaView.without_ui(cache_timeout=None),
            name='schema-json'),
        url(r'^schema/$',
            SchemaView.with_ui('redoc', cache_timeout=None),
            name='schema-redoc'),

        # actual API
        url(r'^', include(router.urls)),

        # should not be picked up by drf-yasg
        path('', include('vng_api_common.api.urls')),
        path('', include('vng_api_common.notifications.api.urls')),
    ])),
]
