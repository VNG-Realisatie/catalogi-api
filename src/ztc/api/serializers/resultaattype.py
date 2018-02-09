from rest_framework_nested.relations import NestedHyperlinkedIdentityField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from ...datamodel.models import ResultaatType
from ..utils.rest_flex_fields import FlexFieldsSerializerMixin
from ..utils.serializers import SourceMappingSerializerMixin


class ResultaatTypeSerializer(FlexFieldsSerializerMixin, SourceMappingSerializerMixin, NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'zaaktype_pk': 'is_relevant_voor__pk',
        'catalogus_pk': 'is_relevant_voor__maakt_deel_uit_van__pk',
    }

    isRelevantVoor = NestedHyperlinkedIdentityField(
        view_name='api:zaaktype-detail',
        source= 'is_relevant_voor',
        parent_lookup_kwargs={
            'catalogus_pk': 'is_relevant_voor__maakt_deel_uit_van__pk',
            'pk': 'is_relevant_voor__pk',
        },
    )
    heeftVerplichtDocumentype = NestedHyperlinkedIdentityField(
        many=True,
        view_name='api:zaakinformatieobjecttype-detail',
        source='heeft_verplichte_ziot',
        parent_lookup_kwargs={
            'catalogus_pk': 'zaaktype__maakt_deel_uit_van__pk',
            'zaaktype_pk': 'zaaktype__pk',
        },
    )
    # TODO: implement relatieklasse serializer first
    # # models.ManyToManyField('datamodel.ZaakInformatieObjectType', through='datamodel.ZaakInformatieobjectTypeArchiefregime'
    # bepaaltAfwijkendArchiefRegimeVan = NestedHyperlinkedIdentityField(
    #     many=True,
    #     view_name='api:zaakinformatieobjecttype-detail',
    #     # source='heeft_verplichte_ziot',
    #     parent_lookup_kwargs={
    #         'catalogus_pk': 'is_relevant_voor__maakt_deel_uit_van__pk',
    #     },
    # )
    leidtTot = NestedHyperlinkedIdentityField(
        many=True,
        view_name='api:besluittype-detail',
        source='leidt_tot',
        parent_lookup_kwargs={
            'catalogus_pk': 'maakt_deel_uit_van__pk',
        },
    )
    heeftVerplichteZaakobjecttype = NestedHyperlinkedIdentityField(
        many=True,
        view_name='api:zaakobjecttype-detail',
        source='heeft_verplichte_zot',
        parent_lookup_kwargs={
            'catalogus_pk': 'is_relevant_voor__maakt_deel_uit_van__pk',
        },
    )
    heeftVoorBrondatumArchiefprocedureRelevante = NestedHyperlinkedIdentityField(
        view_name='api:eigenschap-detail',
        source='heeft_voor_brondatum_archiefprocedure_relevante',
        parent_lookup_kwargs={
            'catalogus_pk': 'is_relevant_voor__maakt_deel_uit_van__pk',
            'zaaktype_pk': 'is_relevant_voor__pk',
            'pk': 'heeft_voor_brondatum_archiefprocedure_relevante__pk'
        },
    )

    class Meta:
        model = ResultaatType

        source_mapping = {
            'ingangsdatumObject': 'datum_begin_geldigheid',
            'einddatumObject': 'datum_einde_geldigheid',

            'omschrijving': 'resultaattypeomschrijving',
            'omschrijvingGeneriek': 'resultaattypeomschrijving_generiek',
            'brondatumProcedure': 'brondatum_archiefprocedure',
            'bepaaltAfwijkendArchiefRegimeVan': 'bepaalt_afwijkend_archiefregime_van',
            'heeftVoorBrondatumArchiefprocedureRelevante': 'heeft_voor_brondatum_archiefprocedure_relevante',
        }
        extra_kwargs = {
            'url': {'view_name': 'api:resultaattype-detail'},
            'heeftVoorBrondatumArchiefprocedureRelevante': {'view_name': 'api:eigenschap-detail'},
        }
        fields = (
            'url',
            'ingangsdatumObject',
            'einddatumObject',

            'omschrijving',
            'omschrijvingGeneriek',
            'selectielijstklasse',
            'archiefnominatie',
            'archiefactietermijn',
            'brondatumProcedure',
            'toelichting',
            'isRelevantVoor',
            'heeftVerplichtDocumentype',
            # 'bepaaltAfwijkendArchiefRegimeVan',
            'leidtTot',
            'heeftVerplichteZaakobjecttype',
            'heeftVoorBrondatumArchiefprocedureRelevante',
        )
