from django.utils.translation import gettext as _

from rest_framework import serializers
from vng_api_common.serializers import add_choice_values_help_text

from ...datamodel.choices import FormaatChoices
from ...datamodel.models import Eigenschap, EigenschapSpecificatie
from ..validators import ZaakTypeConceptValidator
from . import CatalogusSerializer

# class EigenschapReferentieSerializer(SourceMappingSerializerMixin, ModelSerializer):
#     class Meta:
#         model = EigenschapReferentie
#         ref_name = None  # Inline
#         source_mapping = {
#             'pathElement': 'x_path_element',
#         }
#         fields = (
#             'objecttype',
#             'informatiemodel',
#             'namespace',
#             'schemalocatie',
#             'pathElement',
#             'entiteittype',
#         )


class EigenschapSpecificatieSerializer(serializers.ModelSerializer):
    class Meta:
        model = EigenschapSpecificatie
        fields = ("groep", "formaat", "lengte", "kardinaliteit", "waardenverzameling")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        value_display_mapping = add_choice_values_help_text(FormaatChoices)
        self.fields["formaat"].help_text += f"\n\n{value_display_mapping}"

    def validate(self, attrs):
        instance = EigenschapSpecificatie(**attrs)
        instance.clean()
        return attrs


class EigenschapSerializer(serializers.HyperlinkedModelSerializer):

    specificatie = EigenschapSpecificatieSerializer(
        source="specificatie_van_eigenschap"
    )
    zaaktype_identificatie = serializers.SlugRelatedField(
        source="zaaktype", read_only=True, slug_field="identificatie"
    )

    catalogus = serializers.SerializerMethodField()

    class Meta:
        model = Eigenschap
        fields = (
            "url",
            "naam",
            "catalogus",
            "definitie",
            "specificatie",
            "toelichting",
            "zaaktype",
            "zaaktype_identificatie",
            "statustype",
            "begin_geldigheid",
            "einde_geldigheid",
            "begin_object",
            "einde_object",
        )
        extra_kwargs = {
            "url": {"lookup_field": "uuid"},
            "naam": {"source": "eigenschapnaam"},
            "zaaktype": {"lookup_field": "uuid"},
            "statustype": {"lookup_field": "uuid"},
            "begin_object": {"source": "datum_begin_object"},
            "einde_object": {"source": "datum_einde_object"},
            "begin_geldigheid": {
                "source": "datum_begin_geldigheid",
                "help_text": _("De datum waarop de EIGENSCHAP is ontstaan."),
            },
            "einde_geldigheid": {
                "source": "datum_einde_geldigheid",
                "help_text": _("De datum waarop de EIGENSCHAP is opgeheven."),
            },
        }
        validators = [ZaakTypeConceptValidator()]

    def create(self, validated_data):
        specificatie = validated_data.pop("specificatie_van_eigenschap")
        specificatie = EigenschapSpecificatieSerializer().create(specificatie)
        validated_data["specificatie_van_eigenschap"] = specificatie

        eigenschap = super().create(validated_data)
        return eigenschap

    def update(self, instance, validated_data):
        specificatie_data = validated_data.pop("specificatie_van_eigenschap", {})
        if specificatie_data:
            specificatie = instance.specificatie_van_eigenschap
            EigenschapSpecificatieSerializer().update(specificatie, specificatie_data)
        return super().update(instance, validated_data)

    def get_catalogus(self, obj):
        serializer = CatalogusSerializer(
            obj.zaaktype.catalogus,
            many=False,
            context={"request": self.context["request"]},
        ).data
        return serializer["url"]
