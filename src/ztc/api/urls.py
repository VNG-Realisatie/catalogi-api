from django.conf.urls import include, url

from rest_framework_nested import routers

from .schema import schema_view
from .views import CatalogusViewSet, StatusTypeViewSet, ZaakTypeViewSet

root_router = routers.DefaultRouter(trailing_slash=False)
root_router.register(r'catalogussen', CatalogusViewSet)

catalogus_router = routers.NestedSimpleRouter(
    root_router, r'catalogussen',
    lookup='catalogus', trailing_slash=False
)
catalogus_router.register('zaaktypen', ZaakTypeViewSet)

zaaktype_router = routers.NestedSimpleRouter(
    catalogus_router, r'zaaktypen',
    lookup='zaaktype', trailing_slash=False,
)
zaaktype_router.register('statustypen', StatusTypeViewSet)


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
        url(r'^', include(root_router.urls)),
        url(r'^', include(catalogus_router.urls)),
        url(r'^', include(zaaktype_router.urls)),
    ])),
]
