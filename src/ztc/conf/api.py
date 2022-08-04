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

SECURITY_DEFINITION_NAME = "JWT-Claims"

SWAGGER_SETTINGS = BASE_SWAGGER_SETTINGS.copy()
SWAGGER_SETTINGS.update(
    {
        "DEFAULT_INFO": "ztc.api.schema.info",
        "SECURITY_DEFINITIONS": {
            SECURITY_DEFINITION_NAME: {
                # OAS 3.0
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                # not official...
                # 'scopes': {},  # TODO: set up registry that's filled in later...
                # Swagger 2.0
                # 'name': 'Authorization',
                # 'in': 'header'
                # 'type': 'apiKey',
            }
        },
    }
)

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
