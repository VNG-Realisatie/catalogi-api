import os

from django.conf import settings


def get_ztc_oas_spec():
    filepath = os.path.join(settings.BASE_DIR, "src", "openapi.yaml")
    with open(filepath, "rb") as oas_spec:
        return oas_spec.read()
