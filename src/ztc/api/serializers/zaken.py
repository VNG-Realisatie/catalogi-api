from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from rest_framework_nested.relations import NestedHyperlinkedRelatedField

from rest_framework.serializers import (
    HyperlinkedModelSerializer, ModelSerializer
)

from ...datamodel.models import (
    BronCatalogus, BronZaakType, Formulier, ProductDienst, ReferentieProces,
    ZaakObjectType, ZaakType
)
from ..utils.rest_flex_fields import FlexFieldsSerializerMixin
from ..utils.serializers import SourceMappingSerializerMixin


class ZaakObjectTypeSerializer(FlexFieldsSerializerMixin, HyperlinkedModelSerializer):

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
            # 'ingangsdatumObject',
            # 'einddatumObject',
            'objecttype',
            'anderObject',
            'relatieOmschrijving',
            'isRelevantVoor',
            'status_type',  # NOTE: this field is not in the xsd

            # TODO:
            # Not in our datamodel..
            # 'historieMaterieel'  # " type="ztc:ZOT-historieMaterieel" minOccurs="0"
        )


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
    product_dienst = ProductDienstSerializer(many=True, read_only=True)
    formulier = FormulierSerializer(many=True, read_only=True)
    referentieproces = ReferentieProcesSerializer(read_only=True)

    heeftRelevantBesluittype = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='heeft_relevant_besluittype',
        view_name='api:besluittype-detail',
        parent_lookup_kwargs={'catalogus_pk': 'maakt_deel_uit_van__pk'}
    )
    heeftGerelateerd = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='heeft_gerelateerd',
        view_name='api:zaaktype-detail',
        parent_lookup_kwargs={
            'catalogus_pk': 'maakt_deel_uit_van__pk',
        }
    )
    isDeelzaaktypeVan = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='is_deelzaaktype_van',
        view_name='api:zaaktype-detail',
        parent_lookup_kwargs={'catalogus_pk': 'maakt_deel_uit_van__pk'},
    )

    class Meta:
        model = ZaakType
        source_mapping = {
            # "ingangsdatumObject": 'datum_begin_geldigheid',
            # "einddatumObject": 'datum_einde_geldigheid',

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
            # 'heeftRelevantInformatieobjecttype': 'heeft_relevant_informatieobjecttype',
            # 'heeftEigenschap': 'eigenschap_set',
            # 'heeftRelevantZaakObjecttype': 'zaakobjecttype_set',
            # 'heeftRelevantResultaattype': 'resultaattype_set',
            # 'heeftStatustype': 'statustype_set',
            # 'heeftRoltype': 'roltype_set',
        }
        extra_kwargs = {
            'url': {'view_name': 'api:zaaktype-detail'},
            'maaktDeelUitVan': {'view_name': 'api:catalogus-detail'},
        }
        fields = (
            # 'url',
            # 'ingangsdatumObject',
            # 'einddatumObject',
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
        )

        expandable_fields = {
            'maaktDeelUitVan': ('ztc.api.serializers.CatalogusSerializer', {'source': 'maakt_deel_uit_van'}),
        }
