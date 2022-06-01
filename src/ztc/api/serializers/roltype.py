import datetime
from drf_writable_nested import NestedCreateMixin
from rest_framework import serializers
from vng_api_common.constants import RolOmschrijving
from vng_api_common.serializers import add_choice_values_help_text

from ...datamodel.models import RolType
from ..validators import ZaakTypeConceptValidator


class RolTypeSerializer(
    NestedCreateMixin,
    serializers.HyperlinkedModelSerializer,
):
    class Meta:
        model = RolType
        fields = (
            "url",
            "zaaktype",
            "zaaktype_identificatie",
            "omschrijving",
            "omschrijving_generiek",
            "catalogus",
            "begin_geldigheid",
            "einde_geldigheid",
        )

        extra_kwargs = {
            "url": {"lookup_field": "uuid"},
            "zaaktype": {"lookup_field": "uuid"},
            "catalogus": {"lookup_field": "uuid"},
            "begin_geldigheid": {"source": "datum_begin_geldigheid"},
            "einde_geldigheid": {"source": "datum_einde_geldigheid"},
        }
        validators = [ZaakTypeConceptValidator()]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        value_display_mapping = add_choice_values_help_text(RolOmschrijving)
        self.fields["omschrijving_generiek"].help_text += f"\n\n{value_display_mapping}"

    def create(self, validated_data):
        identificatie = validated_data.pop["zaaktype"].identificatie
        validated_data["zaaktype_identificatie"] = identificatie
        roltype = super().create(validated_data)
        return roltype
