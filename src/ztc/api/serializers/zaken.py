from django.utils.translation import ugettext_lazy as _

from rest_framework.serializers import ModelSerializer
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from zds_schema.serializers import GegevensGroepSerializer

from ...datamodel.models import (
    BronCatalogus, BronZaakType, Formulier, ZaakObjectType, ZaakType,
    ZaakTypenRelatie
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


class FormulierSerializer(ModelSerializer):
    class Meta:
        model = Formulier
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


class ReferentieProcesSerializer(GegevensGroepSerializer):
    class Meta:
        model = ZaakType
        gegevensgroep = 'referentieproces'


class ZaakTypenRelatieSerializer(ModelSerializer):
    class Meta:
        model = ZaakTypenRelatie
        fields = (
            'zaaktype',
            'aard_relatie',
            'toelichting'
        )
        extra_kwargs = {
            'zaaktype': {'source': 'gerelateerd_zaaktype'},
        }


class ZaakTypeSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'catalogus_uuid': 'catalogus__uuid',
    }

    # formulier = FormulierSerializer(many=True, read_only=True)
    referentieproces = ReferentieProcesSerializer(
        required=True, help_text=_("Het Referentieproces dat ten grondslag ligt aan dit ZAAKTYPE.")
    )
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
    gerelateerde_zaaktypen = ZaakTypenRelatieSerializer(
        many=True, source='zaaktypenrelaties',
        help_text="De ZAAKTYPEn van zaken die relevant zijn voor zaken van dit ZAAKTYPE."
    )
    # isDeelzaaktypeVan = NestedHyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     source='is_deelzaaktype_van',
    #     view_name='api:zaaktype-detail',
    #     parent_lookup_kwargs={
    #         'catalogus_pk': 'catalogus__pk'
    #     },
    # )
    informatieobjecttypen = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='heeft_relevant_informatieobjecttype',
        view_name='informatieobjecttype-detail',
        lookup_field='uuid',
        parent_lookup_kwargs={
            'catalogus_uuid': 'catalogus__uuid',
        }
    )
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
        label=_("heeft relevante besluittypen"),
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
            'vertrouwelijkheidaanduiding',
            # 'zaakcategorie',
            'doel',
            'aanleiding',
            'toelichting',
            'indicatie_intern_of_extern',
            'handeling_initiator',
            'onderwerp',
            'handeling_behandelaar',
            'doorlooptijd',
            'servicenorm',
            'opschorting_en_aanhouding_mogelijk',
            'verlenging_mogelijk',
            'verlengingstermijn',
            'trefwoorden',
            # 'archiefclassificatiecode',
            # 'vertrouwelijkheidAanduiding',
            # 'verantwoordelijke',
            'publicatie_indicatie',
            'publicatietekst',
            'verantwoordingsrelatie',

            'producten_of_diensten',
            'selectielijst_procestype',
            # 'formulier',
            'referentieproces',
            # 'broncatalogus',
            # 'bronzaaktype',

            # 'ingangsdatumObject',
            # 'versiedatum',
            # 'einddatumObject',

            # relaties
            'catalogus',
            'statustypen',
            'eigenschappen',
            'informatieobjecttypen',
            'roltypen',
            'besluittypen',
            'gerelateerde_zaaktypen',
            # # 'heeftRelevantZaakObjecttype',
            # # 'heeftRelevantResultaattype',
            # # 'isDeelzaaktypeVan',
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
