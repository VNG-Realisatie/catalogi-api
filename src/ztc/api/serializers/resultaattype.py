from rest_framework_nested.relations import (
    NestedHyperlinkedIdentityField, NestedHyperlinkedRelatedField
)
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
        source= '*',
        parent_lookup_kwargs={
            'catalogus_pk': 'is_relevant_voor__maakt_deel_uit_van__pk',
            'pk': 'is_relevant_voor__pk',
        },
    )
    heeftVerplichtDocumentype = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='api:zktiot-detail',
        source='heeft_verplichte_ziot',
        parent_lookup_kwargs={
            'catalogus_pk': 'zaaktype__maakt_deel_uit_van__pk',
            'zaaktype_pk': 'zaaktype__pk',
        },
    )
    bepaaltAfwijkendArchiefRegimeVan = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='api:rstiotarc-detail',
        source='zaakinformatieobjecttypearchiefregime_set',
        parent_lookup_kwargs={
            'catalogus_pk': 'zaak_informatieobject_type__zaaktype__maakt_deel_uit_van__pk',
            'zaaktype_pk': 'zaak_informatieobject_type__zaaktype__pk',
        },
    )
    leidtTot = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='api:besluittype-detail',
        source='leidt_tot',
        parent_lookup_kwargs={
            'catalogus_pk': 'maakt_deel_uit_van__pk',
        },
    )
    heeftVerplichteZaakobjecttype = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='api:zaakobjecttype-detail',
        source='heeft_verplichte_zot',
        parent_lookup_kwargs={
            'catalogus_pk': 'is_relevant_voor__maakt_deel_uit_van__pk',
            'zaaktype_pk': 'is_relevant_voor__pk'
        },
    )

    # FIXME: dit is een foreign key die niet verplicht is. Als hij er niet is
    # krijg je een error in get_url op de heeft_voor_...._relevante.pk want die is None
    heeftVoorBrondatumArchiefprocedureRelevante = NestedHyperlinkedIdentityField(
        view_name='api:eigenschap-detail',
        parent_lookup_kwargs={
            'catalogus_pk': 'heeft_voor_brondatum_archiefprocedure_relevante__is_van__maakt_deel_uit_van__pk',
            'zaaktype_pk': 'heeft_voor_brondatum_archiefprocedure_relevante__is_van__pk',
            'pk': 'heeft_voor_brondatum_archiefprocedure_relevante__pk',
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

            # 'heeftVoorBrondatumArchiefprocedureRelevante': 'heeft_voor_brondatum_archiefprocedure_relevante',
        }
        extra_kwargs = {
            'url': {'view_name': 'api:resultaattype-detail'},
            # 'heeftVoorBrondatumArchiefprocedureRelevante': {'view_name': 'api:eigenschap-detail'},
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
