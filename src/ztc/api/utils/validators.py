from rest_framework.serializers import ValidationError
from django.utils.translation import ugettext_lazy as _


class RelationCatalogValidator:
    code = 'relations-incorrect-catalogus'
    message = _("The {} has catalogus different from created object")

    def __init__(self, relation_field: str, catalogus_field='catalogus'):
        self.relation_field = relation_field
        self.catalogus_field = catalogus_field

    def __call__(self, attrs: dict):
        relations = attrs.get(self.relation_field)
        catalogus = attrs.get(self.catalogus_field)

        if not relations:
            return

        if not isinstance(relations, list):
            relations = [relations]

        for relation in relations:
            if relation.catalogus != catalogus:
                raise ValidationError(self.message.format(self.relation_field), code=self.code)
