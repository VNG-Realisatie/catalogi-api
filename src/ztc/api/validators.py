from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from rest_framework.serializers import ValidationError

from ztc.datamodel.models import ZaakType
from ztc.datamodel.utils import get_overlapping_zaaktypes


class ZaaktypeGeldigheidValidator:
    """
    Validate that the (new) object is unique between a start and end date.

    Empty end date is an open interval, which means that the object cannot
    be created after the start date.
    """

    message = _(
        "Dit zaaktype komt al voor binnen de catalogus en opgegeven geldigheidsperiode."
    )
    code = "overlap"

    def set_context(self, serializer):
        """
        This hook is called by the serializer instance,
        prior to the validation call being made.
        """
        # Determine the existing instance, if this is an update operation.
        self.instance = getattr(serializer, "instance", None)

    def __call__(self, attrs):
        catalogus = attrs.get("catalogus") or self.instance.catalogus
        zaaktype_omschrijving = (
            attrs.get("zaaktype_omschrijving") or self.instance.zaaktype_omschrijving
        )
        datum_begin_geldigheid = (
            attrs.get("datum_begin_geldigheid") or self.instance.datum_begin_geldigheid
        )
        current_einde_geldigheid = (
            self.instance.datum_einde_geldigheid if self.instance is not None else None
        )
        datum_einde_geldigheid = (
            attrs.get("datum_einde_geldigheid") or current_einde_geldigheid
        )

        query = get_overlapping_zaaktypes(
            catalogus,
            zaaktype_omschrijving,
            datum_begin_geldigheid,
            datum_einde_geldigheid,
            self.instance,
        )

        # regel voor zaaktype omschrijving
        if query.exists():
            raise ValidationError({"begin_geldigheid": self.message}, code=self.code)


class ConceptUpdateValidator:
    message = _("Het is niet toegestaan om een non-concept object bij te werken")
    code = "non-concept-object"

    def set_context(self, serializer):
        """
        This hook is called by the serializer instance,
        prior to the validation call being made.
        """
        # Determine the existing instance, if this is an update operation.
        self.instance = getattr(serializer, "instance", None)
        self.request = serializer.context["request"]

    def __call__(self, attrs):
        if not self.instance:
            return

        einde_geldigheid = attrs.get("datum_einde_geldigheid")
        if einde_geldigheid and len(self.request.data) == 1:
            return

        if not self.instance.concept:
            raise ValidationError(self.message, code=self.code)


class ZaakTypeConceptValidator:
    """
    Validator that checks for related non-concept zaaktype when doing
    updates/creates
    """

    message = _(
        "Updating an object that has a relation to a non-concept zaaktype is forbidden"
    )
    code = "non-concept-zaaktype"

    def set_context(self, serializer):
        """
        This hook is called by the serializer instance,
        prior to the validation call being made.
        """
        # Determine the existing instance, if this is an update operation.
        self.instance = getattr(serializer, "instance", None)

    def __call__(self, attrs):
        if self.instance:
            zaaktype = self.instance.zaaktype
            if not zaaktype.concept:
                raise ValidationError(self.message, code=self.code)

        zaaktype_in_attrs = attrs.get("zaaktype")
        if zaaktype_in_attrs:
            if not zaaktype_in_attrs.concept:
                msg = _("Creating a relation to non-concept zaaktype is forbidden")
                raise ValidationError(msg, code=self.code)


class M2MConceptCreateValidator:
    """
    Validator that checks for related non-concepts in M2M fields when creating
    objects
    """

    code = "non-concept-relation"

    def __init__(self, concept_related_fields):
        self.concept_related_fields = concept_related_fields

    def set_context(self, serializer):
        """
        This hook is called by the serializer instance,
        prior to the validation call being made.
        """
        # Determine the existing instance, if this is an update operation.
        self.instance = getattr(serializer, "instance", None)

    def __call__(self, attrs):
        if self.instance:
            return

        for field_name in self.concept_related_fields:
            field = attrs.get(field_name, [])
            for related_object in field:
                if not related_object.concept:
                    msg = _(
                        f"Relations to non-concept {field_name} object can't be created"
                    )
                    raise ValidationError(msg, code=self.code)


class M2MConceptUpdateValidator:
    """
    Validator that checks for related non-concepts in M2M fields when doing
    updates
    """

    code = "non-concept-relation"

    def __init__(self, concept_related_fields):
        self.concept_related_fields = concept_related_fields

    def set_context(self, serializer):
        """
        This hook is called by the serializer instance,
        prior to the validation call being made.
        """
        # Determine the existing instance, if this is an update operation.
        self.instance = getattr(serializer, "instance", None)
        self.request = serializer.context["request"]

    def __call__(self, attrs):
        if not self.instance:
            return

        einde_geldigheid = attrs.get("datum_einde_geldigheid")
        if einde_geldigheid and len(self.request.data) == 1:
            return

        for field_name in self.concept_related_fields:
            field = getattr(self.instance, field_name)
            related_non_concepts = field.filter(concept=False)
            if related_non_concepts.exists():
                msg = _(f"Objects related to non-concept {field_name} can't be updated")
                raise ValidationError(msg, code=self.code)

            # Validate that no new relations are created to resources with
            # non-concept status
            field_in_attrs = attrs.get(field_name)
            if field_in_attrs:
                for relation in field_in_attrs:
                    if not relation.concept:
                        msg = _(
                            f"Objects can't be updated with a relation to non-concept {field_name}"
                        )
                        raise ValidationError(msg, code=self.code)


class ZaakInformatieObjectTypeCatalogusValidator:
    code = "relations-incorrect-catalogus"
    message = _("The zaaktype has catalogus different from informatieobjecttype")

    def set_context(self, serializer):
        """
        This hook is called by the serializer instance,
        prior to the validation call being made.
        """
        self.instance = getattr(serializer, "instance", None)

    def __call__(self, attrs: dict):
        zaaktype = attrs.get("zaaktype") or self.instance.zaaktype
        informatieobjecttype = (
            attrs.get("informatieobjecttype") or self.instance.informatieobjecttype
        )

        if zaaktype.catalogus != informatieobjecttype.catalogus:
            raise ValidationError(self.message, code=self.code)


class DeelzaaktypeCatalogusValidator:
    code = "relations-incorrect-catalogus"
    message = _("Hoofd- en deelzaaktypen moeten tot dezelfde catalogus behoren")

    def set_context(self, serializer):
        """
        This hook is called by the serializer instance,
        prior to the validation call being made.
        """
        self.instance = serializer.instance

    def __call__(self, attrs: dict):
        default_deelzaaktypen = (
            self.instance.deelzaaktypen.all() if self.instance else []
        )
        default_catalogus = self.instance.catalogus if self.instance else None

        deelzaaktypen = attrs.get("deelzaaktypen") or default_deelzaaktypen
        catalogus = attrs.get("catalogus") or default_catalogus

        # can't run validator...
        if catalogus is None:
            return

        if any(
            deelzaaktype.catalogus_id != catalogus.id for deelzaaktype in deelzaaktypen
        ):
            raise ValidationError({"deelzaaktypen": self.message}, code=self.code)
