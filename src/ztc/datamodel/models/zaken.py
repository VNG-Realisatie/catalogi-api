from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ztc.utils.stuff_date import parse_onvolledige_datum
from ..choices import JaNee, ObjectTypen
from .mixins import GeldigheidMixin


class ZaakObjectType(GeldigheidMixin, models.Model):
    """
    De objecttypen van objecten waarop een zaak van het ZAAKTYPE betrekking
    kan hebben.

    Toelichting objecttype
    Een zaak kan op ‘van alles en nog wat’ betrekking hebben.
    Voor zover dit voorkomens (objecten) van de in het RSGB of RGBZ onderscheiden objecttypen
    betreft, wordt met ZAAKOBJECTTYPE gespecificeerd op welke van de RSGB- en/of RGBZ- objecttypen
    zaken van het gerelateerde ZAAKTYPE betrekking kunnen hebben.
    Voor zover het andere objecten betreft, wordt met ZAAKOBJECTTYPE gespecificeerd welke
    andere typen objecten dit betreft.
    """
    # TODO [KING]: objecttype is gespecificeerd als AN40 maar een van de mogelijke waarden
    # (ANDER BUITENLANDS NIET-NATUURLIJK PERSOON) heeft lengte 41. Daarom hebben wij het op max_length=50 gezet
    objecttype = models.CharField(_('objecttype'), max_length=50, help_text=_(
        'De naam van het objecttype waarop zaken van het gerelateerde ZAAKTYPE betrekking hebben.'))
    ander_objecttype = models.CharField(_('ander objecttype'), max_length=1, choices=JaNee.choices, help_text=_(
        'Aanduiding waarmee wordt aangegeven of het ZAAKOBJECTTYPE een ander, niet in RSGB en RGBZ voorkomend, objecttype betreft'))
    relatieomschrijving = models.CharField(_('relatieomschrijving'), max_length=80, help_text=_(
        'Omschrijving van de betrekking van het Objecttype op zaken van het gerelateerde ZAAKTYPE.'))

    # TODO:
    # is_relevant_voor = models.ForeignKey('datamodel.ZaakType', verbose_name=_('is_relevant_voor'), help_text=_(
    #     'Zaken van het ZAAKTYPE waarvoor objecten van dit ZAAKOBJECTTYPE relevant zijn.'))

    class Meta:
        mnemonic = 'ZOT'
        # TODO:
        # unique_together = ('is_relevant_voor', 'objecttype')

    def clean(self):
        """
        Voor het veld objecttype:
        Indien Ander objecttype='N': objecttype moet een van de ObjectTypen zijn
        Indien Ander objecttype='J': alle alfanumerieke tekens

        Datum begin geldigheid:
        - De datum is gelijk aan een Versiedatum van het gerelateerde zaaktype.

        datum einde geldigheid:
        - De datum is gelijk aan of gelegen na de datum zoals opgenomen onder 'Datum begin geldigheid zaakobjecttype’.
        De datum is gelijk aan de dag voor een Versiedatum van het gerelateerde zaaktype.
        """
        if self.ander_objecttype == JaNee.nee and self.objecttype not in ObjectTypen.values.keys():
            raise ValidationError("Indien Ander objecttype='N' moet objecttype een van de objecttypen zijn uit het RSGB of het RGBZ")

        datum_begin = parse_onvolledige_datum(self.datum_begin_geldigheid)
        versiedatum = parse_onvolledige_datum(self.is_relevant_voor.versiedatum)

        if datum_begin != versiedatum:
            raise ValidationError(
                _("De datum_begin_geldigheid moet gelijk zijn aan een Versiedatum van het gerelateerde zaaktype."))

        if self.datum_einde_geldigheid:
            datum_einde = parse_onvolledige_datum(self.datum_einde_geldigheid)

            if datum_einde < datum_begin:
                raise ValidationError(_(
                    "'Datum einde geldigheid' moet gelijk zijn aan of gelegen na de datum zoals opgenomen onder 'Datum begin geldigheid’"))

            if datum_einde + timedelta(days=1) != versiedatum:
                raise ValidationError(_(
                    "'Datum einde geldigheid' moet gelijk zijn aan de dag voor een Versiedatum van het gerelateerde zaaktype."))
