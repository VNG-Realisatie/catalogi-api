from django.conf import settings

from drf_spectacular.extensions import OpenApiSerializerFieldExtension
from notifications_api_common.utils import notification_documentation
from vng_api_common.doc import DOC_AUTH_JWT

from .kanalen import KANAAL_BESLUITTYPEN, KANAAL_INFORMATIEOBJECTTYPEN, KANAAL_ZAAKTYPEN
from .serializers import BesluitTypeSerializer, ZaakTypeSerializer

__all__ = [
    "TITLE",
    "DESCRIPTION",
    "CONTACT",
    "LICENSE",
    "VERSION",
]

TITLE = f"{settings.PROJECT_NAME} API"

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
CONTACT = {
    "email": "standaarden.ondersteuning@vng.nl",
    "url": settings.DOCUMENTATION_URL,
}
LICENSE = {"name": "EUPL 1.2", "url": "https://opensource.org/licenses/EUPL-1.2"}


class HyperlinkedRelatedFieldExtension(OpenApiSerializerFieldExtension):
    target_class = "rest_framework.relations.ManyRelatedField"
    match_subclasses = True

    def map_serializer_field(self, auto_schema, direction):
        default_schema = auto_schema._map_serializer_field(
            self.target, direction, bypass_extensions=True
        )
        if isinstance(self.target.parent, ZaakTypeSerializer):
            if direction == "response":
                default_schema |= {
                    "description": f"URL-referenties naar de BESLUITTYPEN die mogelijk zijn binnen dit ZAAKTYPE."
                }
            else:
                default_schema |= {
                    "description": f"omschrijving-referenties naar de BESLUITTYPEN die mogelijk zijn binnen dit ZAAKTYPE."
                }
                default_schema |= {"example": ["omschrijving"]}
                default_schema |= {"items": {"type": "string", "format": "str"}}
                default_schema |= {"format": "str"}

        if isinstance(self.target.parent, BesluitTypeSerializer):
            if direction == "response":
                default_schema |= {
                    "description": f"URL-referenties naar de BESLUITTYPEN die mogelijk zijn binnen dit ZAAKTYPE."
                }
            else:
                default_schema |= {
                    "description": f"Identificatie-referenties naar de BESLUITTYPEN die mogelijk zijn binnen dit ZAAKTYPE."
                }
                default_schema |= {"example": ["identificaties"]}
                default_schema |= {"items": {"type": "string", "format": "str"}}
                default_schema |= {"format": "str"}

        return {**default_schema, "uniqueItems": True}
