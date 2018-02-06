from rest_framework import serializers, status
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework_nested.relations import NestedHyperlinkedRelatedField

from ...datamodel.models import ZaakType
from ..utils.rest_flex_fields import FlexFieldsSerializerMixin


class ZaakObjectTypeSerializer(FlexFieldsSerializerMixin, serializers.HyperlinkedModelSerializer):
    pass


class ZaakTypeSerializer(FlexFieldsSerializerMixin, serializers.HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:zaaktype-detail')

    class Meta:
        model = ZaakType

        fields = (
            # 'datum_begin_geldigheid',
            # 'datum_einde_geldigheid',

            'zaaktype_identificatie',
            'zaaktype_omschrijving',
            'zaaktype_omschrijving_generiek',
            'zaakcategorie',
            'doel',
            'aanleiding',
            'toelichting',
            'indicatie_intern_of_extern',
            'handeling_initiator',
            'onderwerp',
            'handeling_behandelaar',
            'doorlooptijd_behandeling',
            'servicenorm_behandeling',
            'opschorting_aanhouding_mogelijk',
            'verlenging_mogelijk',
            'verlengingstermijn',
            'trefwoord',  # arrayfield
            'archiefclassificatiecode',
            'vertrouwelijkheidaanduiding',
            'verantwoordelijke',
            'publicatie_indicatie',
            'publicatietekst',
            'verantwoordingsrelatie',
            'versiedatum',

            #
            # groepsattribuutsoorten
            #
            # 'product_dienst',  # m2m ProductDienst
            # 'formulier',  # m2m   Formulier
            # 'referentieproces',  # FK ReferentieProces
            # 'broncatalogus',  # FK  BronCatalogus
            # 'bronzaaktype',  # FK BronZaakType
            #
            # #
            # # relaties
            # #
            # 'heeft_gerelateerd',  # m2m ZaakType
            # 'is_deelzaaktype_van',  # m2m ZaakType
            # 'maakt_deel_uit_van',  # FK catalogus
        )

    # extra_kwargs = {
    #     'is_van': {
    #         'view_name': 'api:zaaktype-detail'
    #     }
    # }



