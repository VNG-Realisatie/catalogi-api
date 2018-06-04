import logging
import os

from django.conf import settings

from drf_yasg import openapi
from rest_framework.settings import api_settings

logger = logging.getLogger(__name__)

try:
    file_path = os.path.join(settings.BASE_DIR, 'docs', 'api', '_description.md')
    with open(file_path, 'r', encoding='utf-8') as f:
        description = f.read()
except FileNotFoundError as e:
    logger.warning('Could not load API documentation description: %s', e)
    description = None


info = openapi.Info(
    title='Zaaktypecatalogus (ZTC) API documentatie',
    default_version='{}'.format(api_settings.DEFAULT_VERSION),
    description=description,
    # terms_of_service='',
    contact=openapi.Contact(email='support@maykinmedia.nl'),
    license=openapi.License(name='EUPL 1.2'),
)
