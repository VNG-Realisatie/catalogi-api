from django.apps import AppConfig


class UtilsConfig(AppConfig):
    name = 'ztc.utils'

    def ready(self):
        from . import checks  # noqa
