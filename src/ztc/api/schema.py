from django.conf import settings

from vng_api_common.doc import DOC_AUTH_JWT
from vng_api_common.notifications.utils import notification_documentation

from .kanalen import KANAAL_BESLUITTYPEN, KANAAL_INFORMATIEOBJECTTYPEN, KANAAL_ZAAKTYPEN

DESCRIPTION = f"""Een API om een zaaktypecatalogus (ZTC) te benaderen.

De zaaktypecatalogus helpt gemeenten om het proces vanuit de 'vraag van een
klant' (productaanvraag, melding, aangifte, informatieverzoek e.d.) tot en met
het leveren van een passend antwoord daarop in te richten, inclusief de
bijbehorende informatievoorziening.

Een CATALOGUS bestaat uit ZAAKTYPEn, INFORMATIEOBJECTTYPEn en BESLUITTYPEn en
wordt typisch gebruikt om een ZAAK (in de Zaken API), INFORMATIEOBJECT (in de
Documenten API) en BESLUIT (in de Besluiten API) te voorzien van type,
standaardwaarden en processtructuur.

**Afhankelijkheden**

Deze API is afhankelijk van:

* Gemeentelijke Selectielijst API
* Autorisaties API *(optioneel)*

{DOC_AUTH_JWT}

### Notificaties

{notification_documentation(KANAAL_ZAAKTYPEN)}

{notification_documentation(KANAAL_BESLUITTYPEN)}

{notification_documentation(KANAAL_INFORMATIEOBJECTTYPEN)}

**Handige links**

* [Documentatie]({settings.DOCUMENTATION_URL}/standaard)
* [Zaakgericht werken]({settings.DOCUMENTATION_URL})
"""

VERSION = settings.API_VERSION
TITLE = f"{settings.PROJECT_NAME} API"
CONTACT = {
    "email": "standaarden.ondersteuning@vng.nl",
    "url": settings.DOCUMENTATION_URL,
}
LICENSE = {"name": "EUPL 1.2", "url": "https://opensource.org/licenses/EUPL-1.2"}
