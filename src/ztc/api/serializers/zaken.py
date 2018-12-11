from rest_framework.serializers import ModelSerializer
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from ...datamodel.models import (
    BronCatalogus, BronZaakType, Formulier, ProductDienst, ReferentieProces,
    ZaakObjectType, ZaakType
)
from ..utils.serializers import SourceMappingSerializerMixin


class ZaakObjectTypeSerializer(SourceMappingSerializerMixin, NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'catalogus_pk': 'is_relevant_voor__catalogus__pk',
        'zaaktype_pk': 'is_relevant_voor__pk',
    }

    isRelevantVoor = NestedHyperlinkedRelatedField(
        read_only=True,
        source='is_relevant_voor',
        view_name='api:zaaktype-detail',
        parent_lookup_kwargs={
            'catalogus_pk': 'catalogus__pk',
        }
    )

    class Meta:
        model = ZaakObjectType
        ref_name = model.__name__
        source_mapping = {
            'ingangsdatumObject': 'datum_begin_geldigheid',
            'einddatumObject': 'datum_einde_geldigheid',
            'anderObject': 'ander_objecttype',
            'relatieOmschrijving': 'relatieomschrijving',
        }
        fields = (
            'url',
            'objecttype',
            'anderObject',
            'relatieOmschrijving',
            'ingangsdatumObject',
            'einddatumObject',
            'isRelevantVoor',
            # NOTE: this field is not in the xsd
            # 'status_type',
        )
        extra_kwargs = {
            'url': {'view_name': 'api:zaakobjecttype-detail'},
        }


class ProductDienstSerializer(ModelSerializer):
    class Meta:
        model = ProductDienst
        ref_name = None  # Inline
        fields = ('naam', 'link')


class FormulierSerializer(ModelSerializer):
    class Meta:
        model = Formulier
        ref_name = None  # Inline
        fields = ('naam', 'link')


class ReferentieProcesSerializer(ModelSerializer):
    class Meta:
        model = ReferentieProces
        ref_name = None  # Inline
        fields = ('naam', 'link')


class BronCatalogusSerializer(ModelSerializer):
    class Meta:
        model = BronCatalogus
        ref_name = None  # Inline
        fields = ('domein', 'rsin')


class BronZaakTypeSerializer(SourceMappingSerializerMixin, ModelSerializer):
    class Meta:
        model = BronZaakType
        ref_name = None  # Inline
        source_mapping = {
            'identificatie': 'zaaktype_identificatie',
            'omschrijving': 'zaaktype_omschrijving',
        }
        fields = (
            'identificatie',
            'omschrijving'
        )


class ZaakTypeSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'catalogus_uuid': 'catalogus__uuid',
    }

    # product_dienst = ProductDienstSerializer(many=True, read_only=True)
    # formulier = FormulierSerializer(many=True, read_only=True)
    # referentieproces = ReferentieProcesSerializer(read_only=True)
    # broncatalogus = BronCatalogusSerializer(read_only=True)
    # bronzaaktype = BronZaakTypeSerializer(read_only=True)

    # heeftRelevantZaakObjecttype = NestedHyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     source='zaakobjecttype_set',
    #     view_name='api:zaakobjecttype-detail',
    #     parent_lookup_kwargs={
    #         'catalogus_pk': 'is_relevant_voor__catalogus__pk',
    #         'zaaktype_pk': 'is_relevant_voor__pk',
    #     }
    # )
    # heeftRelevantBesluittype = NestedHyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     source='heeft_relevant_besluittype',
    #     view_name='api:besluittype-detail',
    #     parent_lookup_kwargs={
    #         'catalogus_pk': 'catalogus__pk'
    #     }
    # )
    # # TODO: currently only show one side of the relations for a ZaakType.
    # heeftGerelateerd = NestedHyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     source='zaaktypenrelatie_van',
    #     view_name='api:zaaktypenrelatie-detail',
    #     parent_lookup_kwargs={
    #         'catalogus_pk': 'zaaktype_van__catalogus__pk',
    #         'zaaktype_pk': 'zaaktype_van__pk',
    #     }
    # )
    # isDeelzaaktypeVan = NestedHyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     source='is_deelzaaktype_van',
    #     view_name='api:zaaktype-detail',
    #     parent_lookup_kwargs={
    #         'catalogus_pk': 'catalogus__pk'
    #     },
    # )
    # heeftRelevantInformatieobjecttype = NestedHyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     source='zaakinformatieobjecttype_set',
    #     view_name='api:zktiot-detail',
    #     parent_lookup_kwargs={
    #         'catalogus_pk': 'zaaktype__catalogus__pk',
    #         'zaaktype_pk': 'zaaktype__pk',
    #     }
    # )
    # heeftRelevantResultaattype = NestedHyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     source='resultaattype_set',
    #     view_name='api:resultaattype-detail',
    #     parent_lookup_kwargs={
    #         'catalogus_pk': 'is_relevant_voor__catalogus__pk',
    #         'zaaktype_pk': 'is_relevant_voor__pk',
    #     }
    # )
    statustypen = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='statustype-detail',
        lookup_field='uuid',
        parent_lookup_kwargs={
            'catalogus_uuid': 'zaaktype__catalogus__uuid',
            'zaaktype_uuid': 'zaaktype__uuid',
        }
    )

    eigenschappen = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='eigenschap_set',
        view_name='eigenschap-detail',
        lookup_field='uuid',
        parent_lookup_kwargs={
            'catalogus_uuid': 'is_van__catalogus__uuid',
            'zaaktype_uuid': 'is_van__uuid'
        },
    )

    roltypen = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='roltype_set',
        view_name='roltype-detail',
        lookup_field='uuid',
        parent_lookup_kwargs={
            'catalogus_uuid': 'zaaktype__catalogus__uuid',
            'zaaktype_uuid': 'zaaktype__uuid'
        },
    )

    besluittypen = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='besluittype_set',
        view_name='besluittype-detail',
        lookup_field='uuid',
        parent_lookup_kwargs={
            'catalogus_uuid': 'catalogus__uuid',
        }
    )

    class Meta:
        model = ZaakType
        fields = (
            'url',
            'identificatie',
            'omschrijving',
            'omschrijving_generiek',
            # 'zaakcategorie',
            # 'doel',
            # 'aanleiding',
            # 'toelichting',
            # 'indicatieInternOfExtern',
            # 'handelingInitiator',
            # 'onderwerp',
            # 'handelingBehandelaar',
            'doorlooptijd',
            'servicenorm',
            # 'opschortingAanhouding',
            # 'verlengingmogelijk',
            # 'verlengingstermijn',
            # 'trefwoord',
            # 'archiefclassificatiecode',
            # 'vertrouwelijkheidAanduiding',
            # 'verantwoordelijke',
            # 'publicatieIndicatie',
            # 'publicatietekst',

            # # groepsattribuutsoorten
            # 'product_dienst',
            # 'formulier',
            # 'referentieproces',
            # 'verantwoordingsrelatie',
            # 'broncatalogus',
            # 'bronzaaktype',

            # 'ingangsdatumObject',
            # 'versiedatum',
            # 'einddatumObject',

            # relaties
            'catalogus',
            'statustypen',
            'eigenschappen',
            'roltypen',
            'besluittypen',
            # # 'heeftRelevantInformatieobjecttype',
            # # 'heeftRelevantBesluittype',
            # # 'heeftRelevantZaakObjecttype',
            # # 'heeftRelevantResultaattype',
            # # 'isDeelzaaktypeVan',
            # # 'heeftGerelateerd',
        )
        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid',
            },
            'identificatie': {
                'source': 'zaaktype_identificatie',
            },
            'omschrijving': {
                'source': 'zaaktype_omschrijving',
            },
            'omschrijving_generiek': {
                'source': 'zaaktype_omschrijving_generiek',
            },
            'catalogus': {
                'lookup_field': 'uuid',
            },
            'doorlooptijd': {
                'source': 'doorlooptijd_behandeling',
            },
            'servicenorm': {
                'source': 'servicenorm_behandeling',
            },
        }

        # expandable_fields = {
        #     'catalogus': ('ztc.api.serializers.CatalogusSerializer', {'source': 'catalogus'}),
        # }
