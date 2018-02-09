from rest_framework_nested.relations import NestedHyperlinkedIdentityField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from ...datamodel.models import ZaakTypenRelatie
from ..utils.rest_flex_fields import FlexFieldsSerializerMixin
from ..utils.serializers import SourceMappingSerializerMixin


class ZaakTypenRelatieSerializer(FlexFieldsSerializerMixin, SourceMappingSerializerMixin, NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'catalogus_pk': 'zaaktype_van__maakt_deel_uit_van__pk',
        'zaaktype_pk': 'zaaktype_van__pk',
    }

    zaaktype_van = NestedHyperlinkedIdentityField(
        view_name='api:zaaktype-detail',
        parent_lookup_kwargs={
            'catalogus_pk': 'zaaktype_van__maakt_deel_uit_van__pk',
            'pk': 'zaaktype_van__pk',
        },
    )
    zaaktype_naar = NestedHyperlinkedIdentityField(
        view_name='api:zaaktype-detail',
        parent_lookup_kwargs={
            'catalogus_pk': 'zaaktype_naar__maakt_deel_uit_van__pk',
            'pk': 'zaaktype_naar__pk',
        },
    )

    # TODO: we don't want 'zaaktype_van' and 'zaaktype_naar' in the response. The fields have to be combined
    # in a list: 'gerelateerden': ['url_zaaktype_van', 'url_zaaktype_naar']
    # gerelateerden = SerializerMethodField()
    #
    # def get_the_url(self, zaaktype):
    #     from rest_framework.reverse import reverse
    #     return reverse('api:zaaktype-detail', kwargs={
    #         'version': 1,  # fix this
    #         'catalogus_pk': zaaktype.maakt_deel_uit_van.pk,
    #         'pk': zaaktype.pk,
    #     })
    # #
    # def get_gerelateerden(self, obj):
    #     return [
    #         self.get_the_url(obj.zaaktype_van),
    #         self.get_the_url(obj.zaaktype_naar),
    #     ]

    class Meta:
        model = ZaakTypenRelatie
        fields = (
            'url',
            'zaaktype_van',
            'zaaktype_naar',
            'aard_relatie',
            'toelichting',
            # 'gerelateerden',
        )
        extra_kwargs = {
            'url': {'view_name': 'api:zaaktypenrelatie-detail'},
        }
