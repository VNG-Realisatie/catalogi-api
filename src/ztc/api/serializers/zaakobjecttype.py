from rest_framework.serializers import HyperlinkedModelSerializer

from ztc.datamodel.models.zaakobjecttype import ZaakObjectType


# TODO doublecheck field help text when creating documentation
class ZaakObjectTypeSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = ZaakObjectType
        fields = (
            "url",
            "ander_objecttype",
            "begin_geldigheid",
            "einde_geldigheid",
            "objecttype",
            "relatie_omschrijving",
            "zaaktype",
            "resultaattypen",
            "statustypen",
            "catalogus",
        )

        extra_kwargs = {
            "url": {"lookup_field": "uuid"},
            "zaaktype": {"lookup_field": "uuid"},
            "resultaattypen": {"lookup_field": "uuid", "read_only": True},
            "statustypen": {"lookup_field": "uuid", "read_only": True},
            "catalogus": {"lookup_field": "uuid"},
            "begin_geldigheid": {"source": "datum_begin_geldigheid"},
            "einde_geldigheid": {"source": "datum_einde_geldigheid"},
        }

    def validate(self, data):
        # this does not include m2m or reverse related fields but those are
        # readonly for this serializer
        model_fields = [field.name for field in self.Meta.model._meta.fields]

        instance = self.Meta.model(
            **{field: value for field, value in data.items() if field in model_fields}
        )
        instance.clean()
        return data
