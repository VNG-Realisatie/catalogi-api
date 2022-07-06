from collections import OrderedDict

from django.utils.translation import ugettext_lazy as _

from rest_framework import exceptions
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler as drf_exception_handler


def exception_handler(exc, context):
    response = drf_exception_handler(exc, context)

    if response is not None:
        data = getattr(response, "data", {})
        request = context.get("request", object)

        response.data = OrderedDict(
            [
                ("type", exc.__class__.__name__),
                ("title", response.status_text),
                ("status", response.status_code),
                ("detail", data.get("detail", "")),
                ("instance", getattr(request, "path", "")),
            ]
        )

        if isinstance(exc, exceptions.ValidationError):
            response.data["invalid_params"] = [
                OrderedDict(
                    [
                        ("type", exc.__class__.__name__),
                        ("name", field_name),
                        ("reason", "; ".join(message)),
                    ]
                )
                for field_name, message in exc.detail.items()
            ]

    return response


class OverlappingException(APIException):
    status_code = 400
    default_detail = _(
        f"De object komt al voor binnen de catalogus en opgegeven geldigheidsperiode."
    )
    default_code = "overlapping-geldigheiden"


class TooManyObjectsReturned(APIException):
    status_code = 400
    default_detail = _(
        f"Het is niet mogelijk om te publiseren als hier meerdere objecten worden terug gegeven"
    )
    default_code = "multiple-objects"
