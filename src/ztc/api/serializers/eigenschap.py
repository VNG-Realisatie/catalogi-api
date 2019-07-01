from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from ztc.datamodel.models import Eigenschap, EigenschapSpecificatie

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
        fields = (
            'groep',
            'formaat',
            'lengte',
            'kardinaliteit',
            'waardenverzameling',
        )


class EigenschapSerializer(serializers.HyperlinkedModelSerializer):

    specificatie = EigenschapSpecificatieSerializer(read_only=True, source='specificatie_van_eigenschap')
    # referentie = EigenschapReferentieSerializer(read_only=True, source='referentie_naar_eigenschap')

    class Meta:
        model = Eigenschap
        fields = (
            'url',
            'naam',
            'definitie',
            'specificatie',
            'toelichting',
            'ingangsdatum_object',
            'einddatum_object',
            'zaaktype',
        )
        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid',
            },
            'ingangsdatum_object': {
                'source': 'datum_begin_geldigheid',
            },
            'einddatum_object': {
                'source': 'datum_einde_geldigheid',
            },
            'naam': {
                'source': 'eigenschapnaam',
            },
            'zaaktype': {
                'lookup_field': 'uuid',
            }
        }
