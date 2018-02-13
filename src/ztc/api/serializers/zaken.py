from rest_framework.serializers import ModelSerializer
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from ...datamodel.models import (
    BronCatalogus, BronZaakType, Formulier, ProductDienst, ReferentieProces,
    ZaakObjectType, ZaakType
)
from ..utils.rest_flex_fields import FlexFieldsSerializerMixin
from ..utils.serializers import SourceMappingSerializerMixin


class ZaakObjectTypeSerializer(SourceMappingSerializerMixin, NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'catalogus_pk': 'is_relevant_voor__maakt_deel_uit_van__pk',
        # 'zaaktype_pk': 'is_relevant_voor__pk', ??
    }

    isRelevantVoor = NestedHyperlinkedRelatedField(
        read_only=True,
        source='*',
        view_name='api:zaaktype-detail',
        parent_lookup_kwargs={
            'catalogus_pk': 'is_relevant_voor__maakt_deel_uit_van__pk',
            'pk': 'is_relevant_voor__pk'}
    )

    class Meta:
        model = ZaakObjectType
        source_mapping = {
            'ingangsdatumObject': 'datum_begin_geldigheid',
            'einddatumObject': 'datum_einde_geldigheid',
            'anderObject': 'ander_objecttype',
            'relatieOmschrijving': 'relatieomschrijving',
            'isRelevantVoor': 'is_relevant_voor',
        }
        fields = (
            'url',
            'ingangsdatumObject',
            'einddatumObject',
            'objecttype',
            'anderObject',
            'relatieOmschrijving',
            'isRelevantVoor',
            'status_type',  # NOTE: this field is not in the xsd
        )
        extra_kwargs = {
            'url': {'view_name': 'api:zaakobjecttype-detail'},
        }


class ProductDienstSerializer(ModelSerializer):
    class Meta:
        model = ProductDienst
        fields = ('naam', 'link')


class FormulierSerializer(ModelSerializer):
    class Meta:
        model = Formulier
        fields = ('naam', 'link')


class ReferentieProcesSerializer(ModelSerializer):
    class Meta:
        model = ReferentieProces
        fields = ('naam', 'link')


class BronCatalogusSerializer(ModelSerializer):
    class Meta:
        model = BronCatalogus
        fields = ('domein', 'rsin')


class BronZaakTypeSerializer(ModelSerializer):
    class Meta:
        model = BronZaakType
        source_mapping = {
            'identificatie': 'zaaktype_identificatie',
            'omschrijving': 'zaaktype_omschrijving',
        }
        fields = (
            'identificatie',
            'omschrijving'
        )


class ZaakTypeSerializer(FlexFieldsSerializerMixin, SourceMappingSerializerMixin, NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'catalogus_pk': 'maakt_deel_uit_van__pk',
    }

    product_dienst = ProductDienstSerializer(many=True, read_only=True)
    formulier = FormulierSerializer(many=True, read_only=True)
    referentieproces = ReferentieProcesSerializer(read_only=True)

    heeftRelevantZaakObjecttype = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='zaakobjecttype_set',
        view_name='api:zaakobjecttype-detail',
        parent_lookup_kwargs={
            'catalogus_pk': 'is_relevant_voor__maakt_deel_uit_van__pk',
        }
    )
    heeftRelevantBesluittype = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='heeft_relevant_besluittype',
        view_name='api:besluittype-detail',
        parent_lookup_kwargs={'catalogus_pk': 'maakt_deel_uit_van__pk'}
    )
    # TODO: currently only show one side of the relations for a ZaakType.
    heeftGerelateerd = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='zaaktypenrelatie_van',
        view_name='api:zaaktypenrelatie-detail',
        parent_lookup_kwargs={
            'catalogus_pk': 'zaaktype_van__maakt_deel_uit_van__pk',
            'zaaktype_pk': 'zaaktype_van__pk',
        }
    )
    isDeelzaaktypeVan = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='is_deelzaaktype_van',
        view_name='api:zaaktype-detail',
        parent_lookup_kwargs={'catalogus_pk': 'maakt_deel_uit_van__pk'},
    )
    heeftEigenschap = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='eigenschap_set',
        view_name='api:eigenschap-detail',
        parent_lookup_kwargs={'catalogus_pk': 'is_van__maakt_deel_uit_van__pk',
                              'zaaktype_pk': 'is_van__pk'},
    )
    heeftRoltype = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='roltype_set',
        view_name='api:roltype-detail',
        parent_lookup_kwargs={'catalogus_pk': 'is_van__maakt_deel_uit_van__pk',
                              'zaaktype_pk': 'is_van__pk'},
    )
    heeftRelevantInformatieobjecttype = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='zaakinformatieobjecttype_set',
        view_name='api:zktiot-detail',
        parent_lookup_kwargs={
            'catalogus_pk': 'zaaktype__maakt_deel_uit_van__pk',
            'zaaktype_pk': 'zaaktype__pk',
        }
    )

    class Meta:
        model = ZaakType
        source_mapping = {
            "ingangsdatumObject": 'datum_begin_geldigheid',
            "einddatumObject": 'datum_einde_geldigheid',

            'identificatie': 'zaaktype_identificatie',
            'omschrijving': 'zaaktype_omschrijving',
            'omschrijvingGeneriek': 'zaaktype_omschrijving_generiek',
            'indicatieInternOfExtern': 'indicatie_intern_of_extern',
            'handelingInitiator': 'handeling_initiator',
            'handelingBehandelaar': 'handeling_behandelaar',
            'doorlooptijd': 'doorlooptijd_behandeling',
            'servicenorm': 'servicenorm_behandeling',
            'opschortingAanhouding': 'opschorting_aanhouding_mogelijk',
            'verlengingmogelijk': 'verlenging_mogelijk',
            'vertrouwelijkheidAanduiding': 'vertrouwelijkheidaanduiding',
            'publicatieIndicatie': 'publicatie_indicatie',
            'heeftGerelateerd': 'heeft_gerelateerd',
            'isDeelzaaktypeVan': 'is_deelzaaktype_van',
            'maaktDeelUitVan': 'maakt_deel_uit_van',

            # unused:
            # 'heeftRelevantResultaattype': 'resultaattype_set',
            # 'heeftStatustype': 'statustype_set',
        }
        extra_kwargs = {
            'url': {'view_name': 'api:zaaktype-detail'},
            'maaktDeelUitVan': {'view_name': 'api:catalogus-detail'},
        }
        fields = (
            'url',
            'ingangsdatumObject',
            'einddatumObject',
            'identificatie',
            'omschrijving',
            'omschrijvingGeneriek',
            'zaakcategorie',
            'doel',
            'aanleiding',
            'toelichting',
            'indicatieInternOfExtern',
            'handelingInitiator',
            'onderwerp',
            'handelingBehandelaar',
            'doorlooptijd',
            'servicenorm',
            'opschortingAanhouding',
            'verlengingmogelijk',
            'verlengingstermijn',
            'trefwoord',
            'archiefclassificatiecode',
            'vertrouwelijkheidAanduiding',
            'verantwoordelijke',
            'publicatieIndicatie',
            'publicatietekst',
            'verantwoordingsrelatie',  # type='ztc:Verantwoordingsrelatie-e' nillable='true' minOccurs='0' maxOccurs='unbounded'/>
            'versiedatum',

            # groepsattribuutsoorten
            'product_dienst',  # m2m ProductDienst  type='ztc:Product_DienstGrp' nillable='true' minOccurs='0' maxOccurs='unbounded'/>
            'formulier',  # m2m Formulier type='ztc:FormulierGrp' nillable='true' minOccurs='0' maxOccurs='unbounded'/>
            'referentieproces',  # FK ReferentieProces type='ztc:ReferentieprocesGrp' nillable='true' minOccurs='0'/>
            'broncatalogus',  # FK  BronCatalogus type='ztc:BroncatalogusGrp' nillable='true' minOccurs='0'/>
            'bronzaaktype',  # FK BronZaakType type='ztc:BronzaaktypeGrp' nillable='true' minOccurs='0'/>

            # relaties
            'heeftGerelateerd',  # m2m ZaakType
            'isDeelzaaktypeVan',  # m2m ZaakType
            'maaktDeelUitVan',  # FK catalogus
            'heeftRelevantBesluittype',
            'heeftEigenschap',
            'heeftRelevantZaakObjecttype',
            'heeftRoltype',
            'heeftRelevantInformatieobjecttype',
        )

        expandable_fields = {
            'maaktDeelUitVan': ('ztc.api.serializers.CatalogusSerializer', {'source': 'maakt_deel_uit_van'}),
        }
