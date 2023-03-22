from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from vng_api_common.serializers import add_choice_values_help_text

from ...datamodel.choices import RichtingChoices
from ...datamodel.models import ZaakInformatieobjectType
from ..validators import ZaakInformatieObjectTypeCatalogusValidator


class ZaakTypeInformatieObjectTypeSerializer(serializers.HyperlinkedModelSerializer):
    """
    Represent a ZaakTypeInformatieObjectType.

    Relatie met informatieobjecttype dat relevant is voor zaaktype.
    """

    zaaktype_identificatie = serializers.SlugRelatedField(
        source="zaaktype",
        read_only=True,
        slug_field="identificatie",
        help_text=_(
            "Unieke identificatie van het ZAAKTYPE binnen de CATALOGUS waarin het ZAAKTYPE voorkomt."
        ),
    )

    informatieobjecttype_omschrijving = serializers.SlugRelatedField(
        source="informatieobjecttype",
        read_only=True,
        slug_field="omschrijving",
        help_text=_(
            "Omschrijving van de aard van informatieobjecten van dit INFORMATIEOBJECTTYPE."
        ),
    )

    catalogus = serializers.HyperlinkedRelatedField(
        source="zaaktype.catalogus",
        read_only=True,
        view_name="catalogus-detail",
        lookup_field="uuid",
    )

    class Meta:
        model = ZaakInformatieobjectType
        fields = (
            "url",
            "zaaktype",
            "zaaktype_identificatie",
            "catalogus",
            "informatieobjecttype",
            "informatieobjecttype_omschrijving",
            "volgnummer",
            "richting",
            "statustype",
        )
        extra_kwargs = {
            "url": {"lookup_field": "uuid"},
            "zaaktype": {"lookup_field": "uuid"},
            "informatieobjecttype": {"lookup_field": "uuid"},
            "statustype": {"lookup_field": "uuid"},
        }
        validators = [
            ZaakInformatieObjectTypeCatalogusValidator(),
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        value_display_mapping = add_choice_values_help_text(RichtingChoices)
        self.fields["richting"].help_text += f"\n\n{value_display_mapping}"

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        allow_action_with_force = self.context.get("allow_action_with_force", False)

        if self.instance:
            zaaktype = validated_data.get("zaaktype") or self.instance.zaaktype
            informatieobjecttype = (
                validated_data.get("informatieobjecttype")
                or self.instance.informatieobjecttype
            )

            if (
                not (zaaktype.concept or informatieobjecttype.concept)
                and not allow_action_with_force
            ):
                message = _("Objects related to non-concept objects can't be updated")
                raise serializers.ValidationError(message, code="non-concept-relation")
        else:
            zaaktype = validated_data.get("zaaktype")
            informatieobjecttype = validated_data.get("informatieobjecttype")

            if (
                not (zaaktype.concept or informatieobjecttype.concept)
                and not allow_action_with_force
            ):
                message = _(
                    "Creating relations between non-concept objects is forbidden"
                )
                raise serializers.ValidationError(message, code="non-concept-relation")

        return validated_data


class ZaakTypeInformatieObjectTypeCreateSerializer(
    ZaakTypeInformatieObjectTypeSerializer
):
    informatieobjecttype = serializers.CharField(
        help_text="`Omschrijvingen` van het INFORMATIEOBJECTTYPE van informatieobjecten waarin besluiten van dit BESLUITTYPE worden vastgelegd."
    )


class ZaakTypeInformatieObjectTypeUpdateSerializer(
    ZaakTypeInformatieObjectTypeCreateSerializer
):
    pass
