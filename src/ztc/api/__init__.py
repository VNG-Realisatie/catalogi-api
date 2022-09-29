default_app_config = "ztc.api.apps.ZTCApiConfig"

from vng_api_common.extensions.fields.duration import DurationFieldExtension
from vng_api_common.extensions.fields.history_url import HistoryURLFieldExtension
from vng_api_common.extensions.fields.hyperlink_identity import (
    HyperlinkedIdentityFieldExtension,
)
from vng_api_common.extensions.fields.many_related import ManyRelatedFieldExtension
from vng_api_common.extensions.fields.read_only import ReadOnlyFieldExtension
from vng_api_common.extensions.filters.query import FilterExtension
from vng_api_common.extensions.serializers.gegevensgroep import GegevensGroepExtension
