from vng_api_common.notifications.kanalen import Kanaal

from ztc.datamodel.models import BesluitType, InformatieObjectType, ZaakType

KANAAL_BESLUITTYPEN = Kanaal(
    'besluittypen',
    main_resource=BesluitType,
    kenmerken=()
)

KANAAL_INFORMATIEOBJECTTYPEN = Kanaal(
    'informatieobjecttypen',
    main_resource=InformatieObjectType,
    kenmerken=()
)

KANAAL_ZAAKTYPEN = Kanaal(
    'zaaktypen',
    main_resource=ZaakType,
    kenmerken=()
)
