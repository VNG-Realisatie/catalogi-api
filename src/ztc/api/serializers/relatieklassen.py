from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from ...datamodel.models import (
    ZaakInformatieobjectType, ZaakInformatieobjectTypeArchiefregime
)
from ..utils.rest_flex_fields import FlexFieldsSerializerMixin
from ..utils.serializers import SourceMappingSerializerMixin


class ZaakTypeInformatieObjectTypeSerializer(FlexFieldsSerializerMixin, SourceMappingSerializerMixin,
                                             NestedHyperlinkedModelSerializer):
    """
    ZKTIOT-basis

    Relatie met informatieobjecttype dat relevant is voor zaaktype.
    """
    parent_lookup_kwargs = {
        'catalogus_pk': 'zaaktype__catalogus__pk',
        'zaaktype_pk': 'zaaktype__pk',
    }

    gerelateerde = NestedHyperlinkedRelatedField(
        read_only=True,
        source='informatie_object_type',
        view_name='api:informatieobjecttype-detail',
        parent_lookup_kwargs={
            'catalogus_pk': 'catalogus__pk',
        },
    )

    class Meta:
        model = ZaakInformatieobjectType
        ref_name = model.__name__
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
            'url': {'view_name': 'api:zktiot-detail'},
        }


class ZaakInformatieobjectTypeArchiefregimeSerializer(FlexFieldsSerializerMixin, SourceMappingSerializerMixin,
                                                      NestedHyperlinkedModelSerializer):
    """
    RSTIOTARC-basis

    Afwijkende archiveringskenmerken van informatieobjecten van een INFORMATIEOBJECTTYPE bij zaken van een ZAAKTYPE op
    grond van resultaten van een RESULTAATTYPE bij dat ZAAKTYPE.
    """
    parent_lookup_kwargs = {
        'catalogus_pk': 'zaak_informatieobject_type__zaaktype__catalogus__pk',
        'zaaktype_pk': 'zaak_informatieobject_type__zaaktype__pk',
    }

    gerelateerde = NestedHyperlinkedRelatedField(
        read_only=True,
        source='zaak_informatieobject_type',
        view_name='api:informatieobjecttype-detail',
        parent_lookup_kwargs={
            'catalogus_pk': 'informatie_object_type__catalogus__pk',
            'pk': 'informatie_object_type__pk'
        },
    )

    class Meta:
        model = ZaakInformatieobjectTypeArchiefregime
        ref_name = model.__name__
        source_mapping = {
            'rstzdt.selectielijstklasse': 'selectielijstklasse',
            'rstzdt.archiefnominatie': 'archiefnominatie',
            'rstzdt.archiefactietermijn': 'archiefactietermijn',
        }

        fields = (
            'url',
            'gerelateerde',
            'rstzdt.selectielijstklasse',
            'rstzdt.archiefnominatie',
            'rstzdt.archiefactietermijn',
        )
        extra_kwargs = {
            'url': {'view_name': 'api:rstiotarc-detail'},
        }
