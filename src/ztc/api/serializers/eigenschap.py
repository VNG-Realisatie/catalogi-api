from rest_framework.serializers import ModelSerializer
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


class EigenschapSpecificatieSerializer(ModelSerializer):
    class Meta:
        model = EigenschapSpecificatie
        fields = (
            'groep',
            'formaat',
            'lengte',
            'kardinaliteit',
            'waardenverzameling',
        )


class EigenschapSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'zaaktype_uuid': 'is_van__uuid',
        'catalogus_uuid': 'is_van__catalogus__uuid',
    }

    specificatie = EigenschapSpecificatieSerializer(read_only=True, source='specificatie_van_eigenschap')
    # referentie = EigenschapReferentieSerializer(read_only=True, source='referentie_naar_eigenschap')

    zaaktype = NestedHyperlinkedRelatedField(
        read_only=True,
        source='is_van',
        view_name='zaaktype-detail',
        lookup_field='uuid',
        parent_lookup_kwargs={
            'catalogus_uuid': 'catalogus__uuid',
        },
    )

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
            }
        }
