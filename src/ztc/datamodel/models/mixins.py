from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ztc.utils.fields import StUFDateField
from ztc.utils.stuff_date import parse_onvolledige_datum


class GeldigheidMixin(models.Model):
    datum_begin_geldigheid = StUFDateField(
        _('datum begin geldigheid'), help_text=_('De datum waarop het is ontstaan.'))
    datum_einde_geldigheid = StUFDateField(
        _('datum einde geldigheid'), blank=True, null=True, help_text=_('De datum waarop het is opgeheven.'))

    class Meta:
        abstract = True

    @property
    def datum_begin_geldigheid_date(self):
        """
        :return: datetime.date or None when the value is not ok
        """
        try:
            return parse_onvolledige_datum(self.datum_begin_geldigheid)
        except ValidationError:
            return None

    @property
    def datum_einde_geldigheid_date(self):
        """
        :return: datetime.date or None when the value is not ok
        """
        try:
            return parse_onvolledige_datum(self.datum_einde_geldigheid)
        except ValidationError:
            return None

    def clean(self):
        """
        Validate the rule
        De datum is gelijk aan of gelegen na de datum zoals opgenomen onder 'Datum begin geldigheid’.

        This rule applies to the following models,
        # TODO: call the super() in the clean of all those models.
        # TODO: add the other rules for begin_ and einde_geldigheid

        - Besluittype
            - begin: De datum is gelijk aan een Versiedatum van een gerelateerd zaaktype.
            - eind: De datum is gelijk aan de dag voor een Versiedatum van een gerelateerd zaaktype.

        - Eigenschap
            - begin: De datum is gelijk aan een Versiedatum van het gerelateerde zaaktype.
            - eind: De datum is gelijk aan de dag voor een Versiedatum van het gerelateerde zaaktype.

        - INFORMATIEOBJECTTYPE
            CHECK
            - begin: De datum is gelijk aan een Versiedatum van een gerelateerd zaaktype
            - einde: De datum is gelijk aan de dag voor een Versiedatum van een gerelateerd zaaktype.

        - ResultaatType
            CHECK
            - begin De datum is gelijk aan een Versiedatum van het gerelateerde zaaktype.
            - De datum is gelijk aan de dag voor een Versiedatum van het gerelateerde zaaktype

        - RolType
            CHECK
            - begin  De datum is gelijk aan een Versiedatum van het gerelateerde zaaktype.
            - De datum is gelijk aan de dag voor een Versiedatum van het gerelateerde zaaktype

        - StatusType
            CHECK
            - begin  De datum is gelijk aan een Versiedatum van het gerelateerde zaaktype.
            - eind  De datum is gelijk aan de dag voor een Versiedatum van het gerelateerde zaaktype.

        - ZaakObjectType
            CHECK
            - begin De datum is gelijk aan een Versiedatum van het gerelateerde zaaktype.
            - De datum is gelijk aan de dag voor een Versiedatum van het gerelateerde zaaktype.

        - ZaakType
            CHECK
            - begin De datum is gelijk aan de vroegste Versiedatum van het zaaktype.
            - eind  GEEN CHECK voor gerelateerd zaaktype
            EXTRA: veld 'versie datum'
            De Versiedatum is gelijk aan of ligt na de Datum begin geldigheid zaaktype en is gelijk aan of ligt voor de Datum einde geldigheid zaaktype

        """
        if self.datum_begin_geldigheid and self.datum_einde_geldigheid:
            if self.datum_begin_geldigheid_date > self.datum_begin_geldigheid_date:
                raise ValidationError(_('Datum einde geldigheid is gelijk aan of gelegen na de datum zoals opgenomen '
                                        'onder Datum begin geldigheid.'))
