from zds_schema.conf.api import BASE_REST_FRAMEWORK, BASE_SWAGGER_SETTINGS

REST_FRAMEWORK = BASE_REST_FRAMEWORK.copy()
REST_FRAMEWORK.update({
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
    'DEFAULT_PAGINATION_CLASS': 'ztc.api.utils.pagination.HALPagination',
    # Filtering
    'SEARCH_PARAM': 'zoek',  # 'search',
    'ORDERING_PARAM': 'sorteer',  # 'ordering',
})


SWAGGER_SETTINGS = BASE_SWAGGER_SETTINGS.copy()
SWAGGER_SETTINGS.update({
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
    'DEFAULT_INFO': 'ztc.api.schema.info',
    # no geo things here
    'DEFAULT_FIELD_INSPECTORS': BASE_SWAGGER_SETTINGS['DEFAULT_FIELD_INSPECTORS'][1:]
})

REST_FRAMEWORK_EXT = {
    'PAGE_PARAM': 'pagina',
    'EXPAND_PARAM': 'expand',
    'EXPAND_ALL_VALUE': 'true',
    'FIELDS_PARAM': 'fields',
}
