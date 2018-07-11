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
        'zaaktype_pk': 'is_van__pk',
        'catalogus_pk': 'is_van__maakt_deel_uit_van__pk',
    }

    specificatie = EigenschapSpecificatieSerializer(read_only=True, source='specificatie_van_eigenschap')
    # referentie = EigenschapReferentieSerializer(read_only=True, source='referentie_naar_eigenschap')

    zaaktype = NestedHyperlinkedRelatedField(
        read_only=True,
        source='is_van',
        view_name='zaaktype-detail',
        parent_lookup_kwargs={
            'catalogus_pk': 'maakt_deel_uit_van__pk',
        },
    )

    class Meta:
        model = Eigenschap
        extra_kwargs = {
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
