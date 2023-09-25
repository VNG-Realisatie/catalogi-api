from django.utils.translation import gettext as _

from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer, ValidationError

from ztc.api.utils.validators import RelationCatalogValidator
from ztc.datamodel.models.zaakobjecttype import ZaakObjectType


class ZaakObjectTypeSerializer(HyperlinkedModelSerializer):
    zaaktype_identificatie = serializers.SlugRelatedField(
        source="zaaktype",
        read_only=True,
        slug_field="identificatie",
        help_text=_(
            "Unieke identificatie van het ZAAKTYPE binnen de CATALOGUS waarin het ZAAKTYPE voorkomt."
        ),
    )

    class Meta:
        model = ZaakObjectType
        fields = (
            "url",
            "ander_objecttype",
            "begin_geldigheid",
            "einde_geldigheid",
            "begin_object",
            "einde_object",
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
                "help_text": _("URL-referenties naar de RESULTAATTYPEN."),
                "required": False,
            },
            "statustypen": {
                "lookup_field": "uuid",
                "help_text": _("URL-referenties naar de STATUSTYPEN."),
                "required": False,
            },
            "catalogus": {"lookup_field": "uuid"},
            "begin_geldigheid": {"source": "datum_begin_geldigheid"},
            "einde_geldigheid": {"source": "datum_einde_geldigheid"},
            "begin_object": {"source": "datum_begin_object"},
            "einde_object": {"source": "datum_einde_object"},
        }

    def validate(self, data):
        # this does not include m2m or reverse related fields but those are
        # readonly for this serializer
        model_fields = [field.name for field in self.Meta.model._meta.fields]

        instance = self.Meta.model(
            **{field: value for field, value in data.items() if field in model_fields}
        )
        instance.clean()
        allow_action_with_force = self.context.get("allow_action_with_force", False)
        if self.instance:

            zaaktype = data.get("zaaktype") or self.instance.zaaktype

            if not zaaktype.concept and not allow_action_with_force:
                message = _("Objects related to non-concept objects can't be updated")
                raise ValidationError(message, code="non-concept-relation")
        else:
            zaaktype = data.get("zaaktype")
            if not zaaktype.concept and not allow_action_with_force:
                message = _(
                    "Creating relations between non-concept objects is forbidden"
                )
                raise ValidationError(message, code="non-concept-relation")

        return data

    validators = [
        RelationCatalogValidator("zaaktype"),
    ]
