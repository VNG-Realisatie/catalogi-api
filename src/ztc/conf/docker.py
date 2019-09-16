import os

from django.core.exceptions import ImproperlyConfigured

os.environ.setdefault("DB_HOST", "db")
os.environ.setdefault("DB_NAME", "postgres")
os.environ.setdefault("DB_USER", "postgres")
os.environ.setdefault("DB_PASSWORD", "")

from .base import *  # noqa isort:skip

# Helper function
missing_environment_vars = []


def getenv(key, default=None, required=False, split=False):
    val = os.getenv(key, default)
    if required and val is None:
        missing_environment_vars.append(key)
    if split and val:
        val = val.split(",")
    return val


#
# Standard Django settings.
#
DEBUG = bool(getenv("DEBUG", False))

ADMINS = getenv("ADMINS", split=True)
MANAGERS = ADMINS

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = getenv("ALLOWED_HOSTS", "*", split=True)

CACHES = {
    "default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"},
    # https://github.com/jazzband/django-axes/blob/master/docs/configuration.rst#cache-problems
    "axes_cache": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"},
}

# Deal with being hosted on a subpath
subpath = getenv("SUBPATH")
if subpath:
    if not subpath.startswith("/"):
        subpath = f"/{subpath}"

    FORCE_SCRIPT_NAME = subpath
    STATIC_URL = f"{FORCE_SCRIPT_NAME}{STATIC_URL}"
    MEDIA_URL = f"{FORCE_SCRIPT_NAME}{MEDIA_URL}"

#
# Additional Django settings
#

# Disable security measures for development
SESSION_COOKIE_SECURE = bool(getenv("SESSION_COOKIE_SECURE", False))
SESSION_COOKIE_HTTPONLY = bool(getenv("SESSION_COOKIE_HTTPONLY", False))
CSRF_COOKIE_SECURE = bool(getenv("CSRF_COOKIE_SECURE", False))

#
# Custom settings
#
ENVIRONMENT = "docker"


if missing_environment_vars:
    raise ImproperlyConfigured(
        "These environment variables are required but missing: {}".format(
            ", ".join(missing_environment_vars)
        )
    )

#
# Library settings
#

# django-axes
AXES_BEHIND_REVERSE_PROXY = False
AXES_CACHE = "axes_cache"
