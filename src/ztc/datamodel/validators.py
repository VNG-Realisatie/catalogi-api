from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _

from ztc.utils.stuff_date import parse_onvolledige_datum


@deconstructible
class KardinaliteitValidator(object):
    """
    Kardinaliteit: gehele getallen groter dan 0, 'N' voor ongelimiteerd
    (Max length of 3 is handled in the CharField)
    """
    def __call__(self, value):
        if value != 'N':
            try:
                error = int(value) <= 0
            except Exception:
                error = True
            if error:
                raise ValidationError(
                    _("Gebruik gehele getallen groter dan 0 of 'N' voor ongelimiteerd"))


@deconstructible
class OnvolledigeDatumValidator(object):
    """
    Indien de waarde niet geparsed kan worden (volgens de regels die gespecificeerd zijn in de
    parse_onvolledige_datum) zal hij worden geinvalideerd
    """
    def __call__(self, value):
        parse_onvolledige_datum(value)
