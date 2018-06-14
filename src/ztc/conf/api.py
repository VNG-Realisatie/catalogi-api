REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication'
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.TokenHasReadWriteScope',
        # 'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    #
    # # Generic view behavior
    'DEFAULT_PAGINATION_CLASS': 'ztc.api.utils.pagination.HALPagination',
    # 'DEFAULT_FILTER_BACKENDS': (
    #     'django_filters.rest_framework.DjangoFilterBackend',
    #     'rest_framework.filters.SearchFilter',
    #     'rest_framework.filters.OrderingFilter',
    # ),
    #
    # # Filtering
    'SEARCH_PARAM': 'zoek',  # 'search',
    'ORDERING_PARAM': 'sorteer',  # 'ordering',
    #
    # Versioning
    'DEFAULT_VERSION': '1',
    'ALLOWED_VERSIONS': ('1', ),
    'VERSION_PARAM': 'version',
    #
    # # Exception handling
    'EXCEPTION_HANDLER': 'ztc.api.utils.exceptions.exception_handler',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

REST_FRAMEWORK_EXT = {
    'PAGE_PARAM': 'pagina',
    'EXPAND_PARAM': 'expand',
    'EXPAND_ALL_VALUE': 'true',
    'FIELDS_PARAM': 'fields',
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'OAuth2': {
            'type': 'oauth2',
            'flow': 'application',
            'tokenUrl': '/oauth2/token/',
            'scopes': {
                'write': 'Schrijftoegang tot de catalogus en gerelateerde objecten.',
                'read': 'Leestoegang tot de catalogus en gerelateerde objecten.'
            }
        },
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        },
    },
    'DEFAULT_AUTO_SCHEMA_CLASS': 'zds_schema.schema.AutoSchema',
    'DEFAULT_INFO': 'ztc.api.schema.info',
}
