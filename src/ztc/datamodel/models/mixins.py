from django.db import models
from django.utils.translation import ugettext_lazy as _

from ...utils.fields import StUFDateField


class GeldigheidMixin(models.Model):
    datum_begin_geldigheid = StUFDateField(
        _('datum begin geldigheid'), help_text=_('De datum waarop het is ontstaan.'))
    datum_einde_geldigheid = StUFDateField(
        _('datum einde geldigheid'), blank=True, null=True, help_text=_('De datum waarop het is opgeheven.'))

    class Meta:
        abstract = True
