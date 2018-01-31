from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField

from ...datamodel.models import Catalogus
from ..utils.rest_flex_fields import FlexFieldsSerializerMixin
from ..utils.serializers import SourceMappingSerializerMixin


class CatalogusSerializer(FlexFieldsSerializerMixin, SourceMappingSerializerMixin, serializers.HyperlinkedModelSerializer):
    """
    Serializer based on ``CAT-basis`` specified in XSD ``ztc0310_ent_basis.xsd``.
    """

    # Nested serializers are shown as URLs, but should be expandable (see below).
    bestaatuitInformatieobjecttype = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='informatieobjecttype_set',
        view_name='api:informatieobjecttype-detail',
        parent_lookup_kwargs={'catalogus_pk': 'maakt_deel_uit_van__pk'}
    )

    bestaatuitBesluittype = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='besluittype_set',
        view_name='api:besluittype-detail',
        parent_lookup_kwargs={'catalogus_pk': 'maakt_deel_uit_van__pk'}
    )

    class Meta:
        model = Catalogus
        source_mapping = {
            'contactpersoonBeheerNaam': 'contactpersoon_beheer_naam',
            'contactpersoonBeheerTelefoonnummer': 'contactpersoon_beheer_telefoonnummer',
            'contactpersoonBeheerEmailadres': 'contactpersoon_beheer_emailadres',
        }
        extra_kwargs = {
            'url': {'view_name': 'api:catalogus-detail'},
        }
        # All fields should be included. Meta data that is not part of the ZTC information model can be left out.
        fields = (
            'url',

            'domein',
            'rsin',
            'contactpersoonBeheerNaam',
            'contactpersoonBeheerTelefoonnummer',
            'contactpersoonBeheerEmailadres',
            # 'bestaatuitZaaktype',
            'bestaatuitInformatieobjecttype',
            'bestaatuitBesluittype',
        )

    expandable_fields = {
        'bestaatuitInformatieobjecttype': ('ztc.api.serializers.InformatieObjectTypeSerializer', {'source': 'informatieobjecttype_set', 'many': True}),
        'bestaatuitBesluittype': ('ztc.api.serializers.BesluitTypeSerializer', {'source': 'besluittype_set', 'many': True}),
    }
