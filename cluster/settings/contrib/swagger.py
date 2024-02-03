from cluster.settings.environment import env

SPECTACULAR_SETTINGS = {
    'TITLE': 'Swagger API',
    'VERSION': '1.0.0',
    'SCHEMA_PATH_PREFIX': '/api/v[0-9]',
    'AUTHENTICATION_WHITELIST': [],
    'SWAGGER_UI_SETTINGS': {
        'filter': True,
        'persistAuthorization': True,
    },
    'COMPONENT_SPLIT_REQUEST': True,
    'SERVE_INCLUDE_SCHEMA': False,
}

SWAGGER_URL = env.str('SWAGGER_URL', None)
