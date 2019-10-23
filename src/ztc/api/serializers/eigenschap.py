from rest_framework import serializers
from vng_api_common.serializers import add_choice_values_help_text

from ...datamodel.choices import FormaatChoices
from ...datamodel.models import Eigenschap, EigenschapSpecificatie
from ..validators import ZaakTypeConceptValidator

# class EigenschapReferentieSerializer(SourceMappingSerializerMixin, ModelSerializer):
#     class Meta:
#         model = EigenschapReferentie
#         ref_name = None  # Inline
#         source_mapping = {
#             'pathElement': 'x_path_element',
#         }
#         fields = (
#             'objecttype',
#             'informatiemodel',
#             'namespace',
#             'schemalocatie',
#             'pathElement',
#             'entiteittype',
#         )


class EigenschapSpecificatieSerializer(serializers.ModelSerializer):
    class Meta:
        model = EigenschapSpecificatie
        fields = ("groep", "formaat", "lengte", "kardinaliteit", "waardenverzameling")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        value_display_mapping = add_choice_values_help_text(FormaatChoices)
        self.fields["formaat"].help_text += f"\n\n{value_display_mapping}"


class EigenschapSerializer(serializers.HyperlinkedModelSerializer):

    specificatie = EigenschapSpecificatieSerializer(
        read_only=True, source="specificatie_van_eigenschap"
    )
    # referentie = EigenschapReferentieSerializer(read_only=True, source='referentie_naar_eigenschap')

    class Meta:
        model = Eigenschap
        fields = ("url", "naam", "definitie", "specificatie", "toelichting", "zaaktype")
        extra_kwargs = {
            "url": {"lookup_field": "uuid"},
            "naam": {"source": "eigenschapnaam"},
            "zaaktype": {"lookup_field": "uuid"},
        }
        validators = [ZaakTypeConceptValidator()]
