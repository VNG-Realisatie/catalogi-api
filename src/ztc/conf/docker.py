from django.core.exceptions import ImproperlyConfigured

from .base import *

# Helper function
missing_environment_vars = []


def getenv(key, default=None, required=False, split=False):
    val = os.getenv(key, default)
    if required and val is None:
        missing_environment_vars.append(key)
    if split and val:
        val = val.split(',')
    return val


#
# Standard Django settings.
#
DEBUG = getenv('DEBUG', False)

ADMINS = getenv('ADMINS', split=True)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'USER': getenv('DATABASE_USER', 'postgres'),
        'NAME': getenv('DATABASE_NAME', 'postgres'),
        'PASSWORD': getenv('DATABASE_PASSWORD', ''),
        'HOST': getenv('DATABASE_USER', 'db'),
        'PORT': getenv('DATABASE_PORT', '5432'),
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = getenv('ALLOWED_HOSTS', '*', split=True)

#
# Additional Django settings
#

# Disable security measures for development
SESSION_COOKIE_SECURE = getenv('SESSION_COOKIE_SECURE', False)
SESSION_COOKIE_HTTPONLY = getenv('SESSION_COOKIE_HTTPONLY', False)
CSRF_COOKIE_SECURE = getenv('CSRF_COOKIE_SECURE', False)

#
# Custom settings
#
ENVIRONMENT = 'docker'

# Override settings with local settings.
try:
    from .local import *
except ImportError:
    pass


if missing_environment_vars:
    raise ImproperlyConfigured(
        'These environment variables are required but missing: {}'.format(', '.join(missing_environment_vars)))
