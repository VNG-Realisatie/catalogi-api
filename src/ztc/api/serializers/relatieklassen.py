from rest_framework_nested.relations import NestedHyperlinkedIdentityField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from ...datamodel.models import ZaakInformatieobjectType, ZaakTypenRelatie
from ..utils.rest_flex_fields import FlexFieldsSerializerMixin
from ..utils.serializers import SourceMappingSerializerMixin


class ZaakTypenRelatieSerializer(FlexFieldsSerializerMixin, SourceMappingSerializerMixin, NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'catalogus_pk': 'zaaktype_van__maakt_deel_uit_van__pk',
        'zaaktype_pk': 'zaaktype_van__pk',
    }

    gerelateerde = NestedHyperlinkedIdentityField(
        view_name='api:zaaktype-detail',
        parent_lookup_kwargs={
            'catalogus_pk': 'zaaktype_naar__maakt_deel_uit_van__pk',
            'pk': 'zaaktype_naar__pk',
        },
    )

    class Meta:
        model = ZaakTypenRelatie
        source_mapping = {
            'aardRelatie': 'aard_relatie',

        }
        fields = (
            'url',
            'aardRelatie',
            'toelichting',
            'gerelateerde',
        )
        extra_kwargs = {
            'url': {'view_name': 'api:zaaktypenrelatie-detail'},
        }


class ZaakInformatieobjectTypeSerializer(FlexFieldsSerializerMixin, SourceMappingSerializerMixin, NestedHyperlinkedModelSerializer):
    """
    IOTZKT-basis
    De relatie naar het zaaktype waarvoor het informatieobjecttype relevant is
    """
    parent_lookup_kwargs = {
        'catalogus_pk': 'zaaktype__maakt_deel_uit_van__pk',
        'zaaktype_pk': 'zaaktype__pk',
    }

    gerelateerde = NestedHyperlinkedIdentityField(
        view_name='api:zaaktype-detail',
        parent_lookup_kwargs={
            'catalogus_pk': 'zaaktype__maakt_deel_uit_van__pk',
            'pk': 'zaaktype__pk',
        },
    )

    class Meta:
        model = ZaakInformatieobjectType

        source_mapping = {
            'zdt.volgnummer': 'volgnummer',
            'zdt.richting': 'richting',
        }

        fields = (
            'url',
            'gerelateerde',
            'zdt.volgnummer',
            'zdt.richting',
        )
        extra_kwargs = {
            'url': {'view_name': 'api:zaakinformatieobjecttype-detail'},
        }



# TODO: in urls:
# iot_router = routers.NestedSimpleRouter(zaaktype_router, r'informatieobjecttypen', lookup='informatieobjecttype')
# iot_router.register(r'is_relevant_voor', ZaakInformatieobjectTypeZKTIOTSerializerViewSet)
class ZaakInformatieobjectTypeZKTIOTSerializer(FlexFieldsSerializerMixin, SourceMappingSerializerMixin, NestedHyperlinkedModelSerializer):
    """
    ZKTIOT-basis

    Relatie met informatieobjecttype dat relevant is voor zaaktype.
    """
    parent_lookup_kwargs = {
        'catalogus_pk': 'zaaktype__maakt_deel_uit_van__pk',
        'zaaktype_pk': 'zaaktype__pk',
    }

    gerelateerde = NestedHyperlinkedIdentityField(
        view_name='api:informatieobjecttype-detail',
        parent_lookup_kwargs={
            'catalogus_pk': 'zaaktype__maakt_deel_uit_van__pk',
            'pk': 'informatie_object_type__pk',
        },
    )

    class Meta:
        model = ZaakInformatieobjectType

        source_mapping = {
            'zdt.volgnummer': 'volgnummer',
            'zdt.richting': 'richting',
        }

        fields = (
            'url',
            'gerelateerde',
            'zdt.volgnummer',
            'zdt.richting',
        )
        extra_kwargs = {
            'url': {'view_name': 'api:zaakinformatieobjecttype-zktiot-detail'},
        }
