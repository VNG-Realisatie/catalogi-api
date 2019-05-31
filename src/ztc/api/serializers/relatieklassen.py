from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from ..utils.rest_flex_fields import FlexFieldsSerializerMixin
from ..utils.serializers import SourceMappingSerializerMixin
from ...datamodel.models import (
    ZaakInformatieobjectType, ZaakInformatieobjectTypeArchiefregime
)


class ZaakTypeInformatieObjectTypeSerializer(serializers.HyperlinkedModelSerializer):
    """
    Represent a ZaakTypeInformatieObjectType.

    Relatie met informatieobjecttype dat relevant is voor zaaktype.
    """
    zaaktype = NestedHyperlinkedRelatedField(
        read_only=True,
        view_name='zaaktype-detail',
        lookup_field='uuid',
        parent_lookup_kwargs={
            'catalogus_uuid': 'catalogus__uuid',
        },
    )
    informatie_object_type = NestedHyperlinkedRelatedField(
        read_only=True,
        view_name='informatieobjecttype-detail',
        lookup_field='uuid',
        parent_lookup_kwargs={
            'catalogus_uuid': 'catalogus__uuid',
        },
    )
    status_type = NestedHyperlinkedRelatedField(
        read_only=True,
        view_name='statustype-detail',
        lookup_field='uuid',
        parent_lookup_kwargs={
            'zaaktype_uuid': 'zaaktype__uuid',
            'catalogus_uuid': 'zaaktype__catalogus__uuid',
        },
    )

    class Meta:
        model = ZaakInformatieobjectType
        fields = (
            'url',
            'zaaktype',
            'informatie_object_type',
            'volgnummer',
            'richting',
            'status_type',
        )
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
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
