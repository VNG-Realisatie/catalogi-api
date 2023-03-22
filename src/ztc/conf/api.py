import os

from vng_api_common.conf.api import *  # noqa - imports white-listed

API_VERSION = "1.3.0"

REST_FRAMEWORK = BASE_REST_FRAMEWORK.copy()
REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = (
    "vng_api_common.permissions.AuthScopesRequired",
)
REST_FRAMEWORK["PAGE_SIZE"] = 100
REST_FRAMEWORK[
    "DEFAULT_PAGINATION_CLASS"
] = "rest_framework.pagination.PageNumberPagination"

SECURITY_DEFINITION_NAME = "JWT-Claims"

DOCUMENTATION_INFO_MODULE = "ztc.api.schema"

SPECTACULAR_SETTINGS = BASE_SPECTACULAR_SETTINGS.copy()
SPECTACULAR_SETTINGS.update(
    {
        # Optional list of servers.
        # Each entry MUST contain "url", MAY contain "description", "variables"
        # e.g. [{'url': 'https://example.com/v1', 'description': 'Text'}, ...]
        "SERVERS": [
            {
                "url": "https://catalogi-api.vng.cloud/api/v1",
                "description": "Productie Omgeving",
            }
        ],
        # todo remove this line below when deploying to production
        "SORT_OPERATION_PARAMETERS": False,
    }
)
SPECTACULAR_EXTENSIONS = [
    "vng_api_common.extensions.fields.duration.DurationFieldExtension",
    "vng_api_common.extensions.fields.history_url.HistoryURLFieldExtension",
    "vng_api_common.extensions.fields.hyperlink_identity.HyperlinkedIdentityFieldExtension",
    "vng_api_common.extensions.fields.many_related.ManyRelatedFieldExtension",
    "vng_api_common.extensions.fields.read_only.ReadOnlyFieldExtension",
    "vng_api_common.extensions.filters.query.FilterExtension",
    "vng_api_common.extensions.serializers.gegevensgroep.GegevensGroepExtension",
]

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
