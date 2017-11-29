from django.utils.translation import ugettext_lazy as _

from ztc.utils.fields import StUFDateField


class GeldigheidMixin(object):
    datum_begin_geldigheid = StUFDateField(
        _('datum begin geldigheid'), help_text=_('De datum waarop het is ontstaan.'))
    datum_einde_geldigheid = StUFDateField(
        _('datum einde geldigheid'), blank=True, null=True, help_text=_('De datum waarop het is opgeheven.'))
