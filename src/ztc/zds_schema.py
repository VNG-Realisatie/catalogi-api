from django.apps import AppConfig


# override to NOT run the default ready events
class ZDSSchemaConfig(AppConfig):
    name = 'zds_schema'
