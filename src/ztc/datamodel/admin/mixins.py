from django.contrib.admin.widgets import AdminDateWidget
from django.utils.translation import ugettext_lazy as _

from ...utils.fields import StUFDateField


class GeldigheidAdminMixin(object):
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        return tuple(fieldsets) + (
            (_('Geldigheid'), {
                'fields': ('datum_begin_geldigheid', 'datum_einde_geldigheid', )
            }),
        )
    #
    # formfield_overrides = {
    #     StUFDateField: {'widget': AdminDateWidget},
    # }
