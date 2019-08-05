from django.apps import AppConfig


class ZTCApiConfig(AppConfig):
    name = 'ztc.api'

    def ready(self):
        # ensure that the metaclass for every viewset has run
        from .views import besluittype, informatieobjecttype, zaken  # noqa
