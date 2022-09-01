from django.conf.urls import url
from django.urls import include, path

from vng_api_common import routers
from vng_api_common.views import SchemaViewAPI, SchemaViewRedoc

from .views import (
    BesluitTypeViewSet,
    CatalogusViewSet,
    EigenschapViewSet,
    InformatieObjectTypeViewSet,
    ResultaatTypeViewSet,
    RolTypeViewSet,
    StatusTypeViewSet,
    ZaakObjectTypeViewSet,
    ZaakTypeInformatieObjectTypeViewSet,
    ZaakTypeViewSet,
)

router = routers.DefaultRouter()
router.register(r"catalogussen", CatalogusViewSet)
router.register(r"zaaktypen", ZaakTypeViewSet)
router.register(r"zaakobjecttypen", ZaakObjectTypeViewSet)
router.register(r"statustypen", StatusTypeViewSet)
router.register(r"eigenschappen", EigenschapViewSet)
router.register(r"roltypen", RolTypeViewSet)
router.register(r"informatieobjecttypen", InformatieObjectTypeViewSet)
router.register(r"besluittypen", BesluitTypeViewSet)
router.register(r"resultaattypen", ResultaatTypeViewSet)
router.register(r"zaaktype-informatieobjecttypen", ZaakTypeInformatieObjectTypeViewSet)


urlpatterns = [
    url(
        r"^v(?P<version>\d+)/",
        include(
            [
                url(
                    r"^schema-redoc/openapi(.json|.yaml)",
                    SchemaViewAPI.as_view(),
                    name="schema-json",
                ),
                url(
                    r"^schema-redoc/",
                    SchemaViewRedoc.as_view(url_name="schema-redoc"),
                    name="schema-redoc",
                ),
                # actual API
                url(r"^", include(router.urls)),
                # should not be picked up by drf-spectacular
                path("", include("vng_api_common.api.urls")),
                path("", include("vng_api_common.notifications.api.urls")),
            ]
        ),
    )
]
