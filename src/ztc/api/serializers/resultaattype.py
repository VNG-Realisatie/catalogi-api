from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from ...datamodel.models import ResultaatType
from ..utils.rest_flex_fields import FlexFieldsSerializerMixin
from ..utils.serializers import SourceMappingSerializerMixin


class ResultaatTypeSerializer(FlexFieldsSerializerMixin, SourceMappingSerializerMixin, NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'zaaktype_pk': 'is_relevant_voor__pk',
        'catalogus_pk': 'is_relevant_voor__catalogus__pk',
    }

    isRelevantVoor = NestedHyperlinkedRelatedField(
        read_only=True,
        source='is_relevant_voor',
        view_name='api:zaaktype-detail',
        parent_lookup_kwargs={
            'catalogus_pk': 'catalogus__pk',
        },
    )
    heeftVerplichtDocumentype = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='heeft_verplichte_ziot',
        view_name='api:zktiot-detail',
        parent_lookup_kwargs={
            'catalogus_pk': 'zaaktype__catalogus__pk',
            'zaaktype_pk': 'zaaktype__pk',
        },
    )
    bepaaltAfwijkendArchiefRegimeVan = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='zaakinformatieobjecttypearchiefregime_set',
        view_name='api:rstiotarc-detail',
        parent_lookup_kwargs={
            'catalogus_pk': 'zaak_informatieobject_type__zaaktype__catalogus__pk',
            'zaaktype_pk': 'zaak_informatieobject_type__zaaktype__pk',
        },
    )
    leidtTot = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='leidt_tot',
        view_name='api:besluittype-detail',
        parent_lookup_kwargs={
            'catalogus_pk': 'catalogus__pk',
        },
    )
    heeftVerplichteZaakobjecttype = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='heeft_verplichte_zot',
        view_name='api:zaakobjecttype-detail',
        parent_lookup_kwargs={
            'catalogus_pk': 'is_relevant_voor__catalogus__pk',
            'zaaktype_pk': 'is_relevant_voor__pk'
        },
    )

    heeftVoorBrondatumArchiefprocedureRelevante = NestedHyperlinkedRelatedField(
        read_only=True,
        source='heeft_voor_brondatum_archiefprocedure_relevante',
        view_name='api:eigenschap-detail',
        parent_lookup_kwargs={
            'catalogus_pk': 'is_van__catalogus__pk',
            'zaaktype_pk': 'is_van__pk',
        },
    )

    class Meta:
        model = ResultaatType
        ref_name = model.__name__
        source_mapping = {
            'ingangsdatumObject': 'datum_begin_geldigheid',
            'einddatumObject': 'datum_einde_geldigheid',

            'omschrijving': 'resultaattypeomschrijving',
            'omschrijvingGeneriek': 'resultaattypeomschrijving_generiek',
            'brondatumProcedure': 'brondatum_archiefprocedure',
        }
        extra_kwargs = {
            'url': {'view_name': 'api:resultaattype-detail'},
        }
        fields = (
            'url',
            'omschrijving',
            'omschrijvingGeneriek',
            'selectielijstklasse',
            'archiefnominatie',
            'archiefactietermijn',
            'brondatumProcedure',
            'toelichting',

            'ingangsdatumObject',
            'einddatumObject',

            'isRelevantVoor',
            'heeftVerplichtDocumentype',
            'bepaaltAfwijkendArchiefRegimeVan',
            'leidtTot',
            'heeftVerplichteZaakobjecttype',
            'heeftVoorBrondatumArchiefprocedureRelevante',
        )
