from zds_schema.conf.api import *  # noqa - imports white-listed

REST_FRAMEWORK = BASE_REST_FRAMEWORK.copy()
REST_FRAMEWORK.update({
    'DEFAULT_PERMISSION_CLASSES': (
        'zds_schema.permissions.ActionScopesRequired',
    ),
    'DEFAULT_PAGINATION_CLASS': 'ztc.api.utils.pagination.HALPagination',
    # Filtering
    'SEARCH_PARAM': 'zoek',  # 'search',
    'ORDERING_PARAM': 'sorteer',  # 'ordering',
})

SECURITY_DEFINITION_NAME = 'JWT-Claims'

SWAGGER_SETTINGS = BASE_SWAGGER_SETTINGS.copy()
SWAGGER_SETTINGS.update({
    'DEFAULT_INFO': 'ztc.api.schema.info',

    'SECURITY_DEFINITIONS': {
        SECURITY_DEFINITION_NAME: {
            # OAS 3.0
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
            # not official...
            # 'scopes': {},  # TODO: set up registry that's filled in later...

            # Swagger 2.0
            # 'name': 'Authorization',
            # 'in': 'header'
            # 'type': 'apiKey',
        }
    },

    # no geo things here
    'DEFAULT_FIELD_INSPECTORS': BASE_SWAGGER_SETTINGS['DEFAULT_FIELD_INSPECTORS'][1:]
})

REST_FRAMEWORK_EXT = {
    'PAGE_PARAM': 'pagina',
    'EXPAND_PARAM': 'expand',
    'EXPAND_ALL_VALUE': 'true',
    'FIELDS_PARAM': 'fields',
}

GEMMA_URL_INFORMATIEMODEL = 'Imztc'
GEMMA_URL_INFORMATIEMODEL_VERSIE = '2.1'
