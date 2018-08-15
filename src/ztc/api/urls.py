from django.conf.urls import include, url

from zds_schema import routers

from .schema import schema_view
from .views import (
    CatalogusViewSet, EigenschapViewSet, RolTypeViewSet, StatusTypeViewSet,
    ZaakTypeViewSet
)

router = routers.DefaultRouter()
router.register(r'catalogussen', CatalogusViewSet, [
    routers.nested('zaaktypen', ZaakTypeViewSet, [
        routers.nested('statustypen', StatusTypeViewSet),
        routers.nested('eigenschappen', EigenschapViewSet),
        routers.nested('roltypen', RolTypeViewSet),
    ])
])


urlpatterns = [
    url(r'^v(?P<version>\d+)/', include([

        # API documentation
        url(r'^schema/openapi(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=None),
            name='schema-json'),
        url(r'^schema/$',
            schema_view.with_ui('redoc', cache_timeout=None),
            name='schema-redoc'),

        # actual API
        url(r'^', include(router.urls)),
    ])),
]
