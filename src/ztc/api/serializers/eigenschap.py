from rest_framework.serializers import (
    HyperlinkedModelSerializer, ModelSerializer
)
from rest_framework_nested.relations import NestedHyperlinkedIdentityField

from ...datamodel.models import (
    Eigenschap, EigenschapReferentie, EigenschapSpecificatie
)
from ..utils.rest_flex_fields import FlexFieldsSerializerMixin
from ..utils.serializers import SourceMappingSerializerMixin


class EigenschapReferentieSerializer(SourceMappingSerializerMixin, ModelSerializer):
    class Meta:
        model = EigenschapReferentie
        source_mapping = {
            'pathElement': 'x_path_element',
        }
        fields = (
            'objecttype',
            'informatiemodel',
            'namespace',
            'schemalocatie',
            'pathElement',
            'entiteittype',
        )


class EigenschapSpecificatieSerializer(SourceMappingSerializerMixin, ModelSerializer):
    class Meta:
        model = EigenschapSpecificatie
        source_mapping = {
            'waardeverzameling': 'waardenverzameling',
        }
        fields = (
            'groep',
            'formaat',
            'lengte',
            'kardinaliteit',
            'waardeverzameling',
        )


class EigenschapSerializer(FlexFieldsSerializerMixin, SourceMappingSerializerMixin, HyperlinkedModelSerializer):
    specificatie = EigenschapSpecificatieSerializer(read_only=True, source='specificatie_van_eigenschap')
    referentie = EigenschapReferentieSerializer(read_only=True, source='referentie_naar_eigenschap')

    isVan = NestedHyperlinkedIdentityField(
        view_name='api:zaaktype-detail',
        parent_lookup_kwargs={
            'catalogus_pk': 'is_van__maakt_deel_uit_van__pk',
            'pk': 'is_van__pk'
        },
    )

    class Meta:
        model = Eigenschap

        source_mapping = {
            'ingangsdatumObject': 'datum_begin_geldigheid',
            'einddatumObject': 'datum_einde_geldigheid',
            'naam': 'eigenschapnaam',
        }
        fields = (
            'naam',
            'definitie',
            'toelichting',
            'status_type',
            'specificatie',
            'referentie',
            'isVan',
        )
