import os

from vng_api_common.conf.api import *  # noqa - imports white-listed

API_VERSION = "1.2.0-rc5"

REST_FRAMEWORK = BASE_REST_FRAMEWORK.copy()
REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = (
    "vng_api_common.permissions.AuthScopesRequired",
)
REST_FRAMEWORK["PAGE_SIZE"] = 100
REST_FRAMEWORK[
    "DEFAULT_PAGINATION_CLASS"
] = "rest_framework.pagination.PageNumberPagination"

REST_FRAMEWORK["DEFAULT_SCHEMA_CLASS"] = "vng_api_common.inspectors.view.AutoSchema"

SECURITY_DEFINITION_NAME = "JWT-Claims"

SPECTACULAR_SETTINGS = {
    "TAGS": [
        {
            "name": "besluittypen",
            "path": "ztc.api.views.besluittype",
            "view": "BesluitTypeViewSet",
        },
        {
            "name": "catalogussen",
            "path": "ztc.api.views.catalogus",
            "view": "CatalogusViewSet",
        },
        {
            "name": "eigenschappen",
            "path": "ztc.api.views.eigenschap",
            "view": "EigenschapViewSet",
        },
        {
            "name": "informatieobjecttypen",
            "path": "ztc.api.views.informatieobjecttype",
            "view": "InformatieObjectTypeViewSet",
        },
        {
            "name": "zaaktype-informatieobjecttypen",
            "path": "ztc.api.views.relatieklassen",
            "view": "ZaakTypeInformatieObjectTypeViewSet",
        },
        {
            "name": "resultaattypen",
            "path": "ztc.api.views.resultaattype",
            "view": "ResultaatTypeViewSet",
        },
        {"name": "roltypen", "path": "ztc.api.views.roltype", "view": "RolTypeViewSet"},
        {
            "name": "statustypen",
            "path": "ztc.api.views.statustype",
            "view": "StatusTypeViewSet",
        },
        {
            "name": "zaakobjecttypen",
            "path": "ztc.api.views.zaakobjecttype",
            "view": "ZaakObjectTypeViewSet",
        },
        {"name": "zaaktypen", "path": "ztc.api.views.zaken", "view": "ZaakTypeViewSet"},
    ],
    "DESCRIPTION": "ztc.api.schema",
    "SCHEMA_PATH_PREFIX": "/api/v1",
    "SERVERS": [{"url": "/api/v1"}],
    "DEFAULT_GENERATOR_CLASS": "vng_api_common.generators.OpenAPISchemaGenerator",
    "PREPROCESSING_HOOKS": ["vng_api_common.utils.preprocessing_filter_spec"],
    "APPEND_COMPONENTS": {
        "securitySchemes": {
            "JWT-Claims": {
                "type": "http",
                "bearerFormat": "JWT",
                "scheme": "bearer",
            }
        },
    },
    "SECURITY": [
        {
            "JWT-Claims": [],
        }
    ],
}
GEMMA_URL_INFORMATIEMODEL = "Imztc"
GEMMA_URL_INFORMATIEMODEL_VERSIE = "2.1"

repo = "VNG-Realisatie/VNG-referentielijsten"
commit = "da1b2cfdaadb2d19a7d3fc14530923913a2560f2"
REFERENTIELIJSTEN_API_SPEC = (
    f"https://raw.githubusercontent.com/{repo}/{commit}/src/openapi.yaml"  # noqa
)

SELF_REPO = "VNG-Realisatie/catalogi-api"
SELF_BRANCH = os.getenv("SELF_BRANCH") or API_VERSION
GITHUB_API_SPEC = f"https://raw.githubusercontent.com/{SELF_REPO}/{SELF_BRANCH}/src/openapi.yaml"  # noqa
