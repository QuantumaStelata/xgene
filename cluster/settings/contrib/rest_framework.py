from rest_framework import ISO_8601

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_PAGINATION_CLASS': 'generic.paginations.BasePagination',
    'DATE_INPUT_FORMATS': (ISO_8601, '%d.%m.%Y'),
    'DATETIME_INPUT_FORMATS': (ISO_8601, '%d.%m.%Y %H:%M:%S'),
    'COERCE_DECIMAL_TO_STRING': False,
}
