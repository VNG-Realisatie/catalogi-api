from rest_framework_nested.relations import NestedHyperlinkedRelatedField

from ...datamodel.models import Catalogus
from .base import ModelSerializer


class CatalogusSerializer(ModelSerializer):
    """
    Serializer based on ``CAT-basis`` specified in XSD ``ztc0310_ent_basis.xsd``.
    """
    # bestaatuitInformatieobjecttype = NestedHyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     source='informatieobjecttype_set',
    #     view_name='api:informatieobjecttype-detail',
    #     parent_lookup_kwargs={'catalogus_pk': 'maakt_deel_uit_van__pk'}
    # )

    # bestaatuitBesluittype = NestedHyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     source='besluittype_set',
    #     view_name='api:besluittype-detail',
    #     parent_lookup_kwargs={'catalogus_pk': 'maakt_deel_uit_van__pk'}
    # )

    bestaatuitZaaktype = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='zaaktype_set',
        view_name='api:zaaktype-detail',
        parent_lookup_kwargs={'catalogus_pk': 'maakt_deel_uit_van__pk'},
    )

    class Meta:
        model = Catalogus
        ref_name = model.__name__
        source_mapping = {
            'contactpersoonBeheerNaam': 'contactpersoon_beheer_naam',
            'contactpersoonBeheerTelefoonnummer': 'contactpersoon_beheer_telefoonnummer',
            'contactpersoonBeheerEmailadres': 'contactpersoon_beheer_emailadres',
        }
        extra_kwargs = {
            'url': {'view_name': 'api:catalogus-detail'},
        }
        fields = (
            'url',

            'domein',
            'rsin',
            'contactpersoonBeheerNaam',
            'contactpersoonBeheerTelefoonnummer',
            'contactpersoonBeheerEmailadres',
            'bestaatuitZaaktype',
            # 'bestaatuitInformatieobjecttype',
            # 'bestaatuitBesluittype',
        )

    expandable_fields = {
        # 'bestaatuitInformatieobjecttype': (
        #     'ztc.api.serializers.InformatieObjectTypeSerializer',
        #     {'source': 'informatieobjecttype_set', 'many': True}
        # ),
        # 'bestaatuitBesluittype': (
        #     'ztc.api.serializers.BesluitTypeSerializer',
        #     {'source': 'besluittype_set', 'many': True}
        # ),
        'bestaatuitZaaktype': (
            'ztc.api.serializers.ZaakTypeSerializer',
            {'source': 'zaaktype_set', 'many': True}
        )
    }
