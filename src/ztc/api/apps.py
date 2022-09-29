from django.apps import AppConfig

from vng_api_common.api import register_extensions


class ZTCApiConfig(AppConfig):
    name = "ztc.api"

    def ready(self):
        # ensure that the metaclass for every viewset has run
        register_extensions()

        from .views import besluittype, informatieobjecttype, zaken  # noqa
