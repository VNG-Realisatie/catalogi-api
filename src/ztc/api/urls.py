from django.conf.urls import url
from django.urls import include, path

from zds_schema import routers
from zds_schema.schema import SchemaView

from .views import (
    BesluitTypeViewSet, CatalogusViewSet, EigenschapViewSet,
    InformatieObjectTypeViewSet, RolTypeViewSet, StatusTypeViewSet,
    ZaakTypeViewSet
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
        path('', include('zds_schema.api.urls')),
    ])),
]
