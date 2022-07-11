from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from vng_api_common.serializers import add_choice_values_help_text

from ...datamodel.choices import RichtingChoices
from ...datamodel.models import ZaakInformatieobjectType
from ..validators import ZaakInformatieObjectTypeCatalogusValidator


class ZaakTypeInformatieObjectTypeSerializer(serializers.HyperlinkedModelSerializer):
    """
    Represent a ZaakTypeInformatieObjectType.

    Relatie met informatieobjecttype dat relevant is voor zaaktype.
    """

    zaaktype_identificatie = serializers.SlugRelatedField(
        source="zaaktype", read_only=True, slug_field="identificatie"
    )

    informatieobjecttype_omschrijving = serializers.SlugRelatedField(
        source="informatieobjecttype", read_only=True, slug_field="omschrijving"
    )

    class Meta:
        model = ZaakInformatieobjectType
        fields = (
            "url",
            "zaaktype",
            "zaaktype_identificatie",
            "catalogus",
            "informatieobjecttype",
            "informatieobjecttype_omschrijving",
            "volgnummer",
            "richting",
            "statustype",
        )
        extra_kwargs = {
            "url": {"lookup_field": "uuid"},
            "zaaktype": {"lookup_field": "uuid"},
            "informatieobjecttype": {"lookup_field": "uuid"},
            "statustype": {"lookup_field": "uuid"},
            "catalogus": {"lookup_field": "uuid"},
        }
        validators = [
            ZaakInformatieObjectTypeCatalogusValidator(),
            UniqueTogetherValidator(
                queryset=ZaakInformatieobjectType.objects.all(),
                fields=["zaaktype", "volgnummer"],
            ),
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        value_display_mapping = add_choice_values_help_text(RichtingChoices)
        self.fields["richting"].help_text += f"\n\n{value_display_mapping}"

    def validate(self, attrs):
        super().validate(attrs)

        if self.instance:
            zaaktype = attrs.get("zaaktype") or self.instance.zaaktype
            informatieobjecttype = (
                attrs.get("informatieobjecttype") or self.instance.informatieobjecttype
            )

            if not (zaaktype.concept or informatieobjecttype.concept):
                message = _("Objects related to non-concept objects can't be updated")
                raise serializers.ValidationError(message, code="non-concept-relation")
        else:
            zaaktype = attrs.get("zaaktype")
            informatieobjecttype = attrs.get("informatieobjecttype")

            if not (zaaktype.concept or informatieobjecttype.concept):
                message = _(
                    "Creating relations between non-concept objects is forbidden"
                )
                raise serializers.ValidationError(message, code="non-concept-relation")

        return attrs


# class ZaakInformatieobjectTypeArchiefregimeSerializer(FlexFieldsSerializerMixin, SourceMappingSerializerMixin,
#                                                       NestedHyperlinkedModelSerializer):
#     """
#     RSTIOTARC-basis
#
#     Afwijkende archiveringskenmerken van informatieobjecten van een INFORMATIEOBJECTTYPE bij zaken van een ZAAKTYPE op
#     grond van resultaten van een RESULTAATTYPE bij dat ZAAKTYPE.
#     """
#     parent_lookup_kwargs = {
#         'catalogus_pk': 'zaak_informatieobject_type__zaaktype__catalogus__pk',
#         'zaaktype_pk': 'zaak_informatieobject_type__zaaktype__pk',
#     }
#
#     gerelateerde = NestedHyperlinkedRelatedField(
#         read_only=True,
#         source='zaak_informatieobject_type',
#         view_name='api:informatieobjecttype-detail',
#         parent_lookup_kwargs={
#             'catalogus_pk': 'informatieobjecttype__catalogus__pk',
#             'pk': 'informatieobjecttype__pk'
#         },
#     )
#
#     class Meta:
#         model = ZaakInformatieobjectTypeArchiefregime
#         ref_name = model.__name__
#         source_mapping = {
#             'rstzdt.selectielijstklasse': 'selectielijstklasse',
#             'rstzdt.archiefnominatie': 'archiefnominatie',
#             'rstzdt.archiefactietermijn': 'archiefactietermijn',
#         }
#
#         fields = (
#             'url',
#             'gerelateerde',
#             'rstzdt.selectielijstklasse',
#             'rstzdt.archiefnominatie',
#             'rstzdt.archiefactietermijn',
#         )
#         extra_kwargs = {
#             'url': {'view_name': 'api:rstiotarc-detail'},
#         }
