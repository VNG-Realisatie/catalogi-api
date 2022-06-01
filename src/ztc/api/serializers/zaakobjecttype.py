from django.utils.translation import gettext as _

from rest_framework.serializers import HyperlinkedModelSerializer, ValidationError

from ztc.api.utils.validators import RelationCatalogValidator
from ztc.datamodel.models.zaakobjecttype import ZaakObjectType


class ZaakObjectTypeSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = ZaakObjectType
        fields = (
            "url",
            "ander_objecttype",
            "begin_geldigheid",
            "einde_geldigheid",
            "objecttype",
            "relatie_omschrijving",
            "zaaktype",
            "zaaktype_identificatie",
            "resultaattypen",
            "statustypen",
            "catalogus",
        )

        extra_kwargs = {
            "url": {"lookup_field": "uuid"},
            "zaaktype": {"lookup_field": "uuid"},
            "resultaattypen": {
                "lookup_field": "uuid",
                "read_only": True,
                "help_text": _("URL-referenties naar de RESULTAATTYPEN."),
            },
            "statustypen": {
                "lookup_field": "uuid",
                "read_only": True,
                "help_text": _("URL-referenties naar de STATUSTYPEN."),
            },
            "catalogus": {"lookup_field": "uuid"},
            "begin_geldigheid": {"source": "datum_begin_geldigheid"},
            "einde_geldigheid": {"source": "datum_einde_geldigheid"},
        }

    def validate(self, data):
        # this does not include m2m or reverse related fields but those are
        # readonly for this serializer
        model_fields = [field.name for field in self.Meta.model._meta.fields]

        instance = self.Meta.model(
            **{field: value for field, value in data.items() if field in model_fields}
        )
        instance.clean()

        if self.instance:
            zaaktype = data.get("zaaktype") or self.instance.zaaktype

            if not zaaktype.concept:
                message = _("Objects related to non-concept objects can't be updated")
                raise ValidationError(message, code="non-concept-relation")
        else:
            zaaktype = data.get("zaaktype")

            if not zaaktype.concept:
                message = _(
                    "Creating relations between non-concept objects is forbidden"
                )
                raise ValidationError(message, code="non-concept-relation")

        return data

    validators = [
        RelationCatalogValidator("zaaktype"),
    ]

    def create(self, validated_data):
        identificatie = validated_data.pop["zaaktype"].identificatie
        validated_data["zaaktype_identificatie"] = identificatie
        zaakobjecttype = super().create(validated_data)
        return zaakobjecttype
