from drf_writable_nested import NestedCreateMixin
from rest_framework import serializers
from vng_api_common.constants import RolOmschrijving
from vng_api_common.serializers import add_choice_values_help_text

from ...datamodel.models import RolType
from ..validators import ZaakTypeConceptValidator
from .zaken import ZaakTypeSerializer


class RolTypeSerializer(
    NestedCreateMixin,
    serializers.HyperlinkedModelSerializer,
    serializers.ModelSerializer,
):
    # zaaktype = serializers.RelatedField(
    #     many=False, read_only=True, slug_field="identificatie"
    # )
    # zaaktype = serializers.StringRelatedField(many=True)
    zaaktype = ZaakTypeSerializer(many=True, read_only=True)

    class Meta:
        model = RolType
        fields = (
            "url",
            "zaaktype",
            "omschrijving",
            "omschrijving_generiek",
            "catalogus",
            "begin_geldigheid",
            "einde_geldigheid",
        )

        extra_kwargs = {
            "url": {"lookup_field": "uuid"},
            "catalogus": {"lookup_field": "uuid"},
            "begin_geldigheid": {"source": "datum_begin_geldigheid"},
            "einde_geldigheid": {"source": "datum_einde_geldigheid"},
        }
        validators = [ZaakTypeConceptValidator()]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        value_display_mapping = add_choice_values_help_text(RolOmschrijving)
        self.fields["omschrijving_generiek"].help_text += f"\n\n{value_display_mapping}"
