from django.utils.translation import ugettext_lazy as _

from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ValidationError


class ConceptPublishMixin:
    @swagger_auto_schema(request_body=no_body)
    @action(detail=True, methods=["post"])
    def publish(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.concept = False
        instance.save()

        serializer = self.get_serializer(instance)

        return Response(serializer.data)


class ConceptDestroyMixin:
    def get_concept(self, instance):
        return instance.concept

    def perform_destroy(self, instance):
        if not self.get_concept(instance):
            msg = _("Alleen concepten kunnen worden verwijderd.")
            raise ValidationError({"nonFieldErrors": msg}, code="non-concept-object")

        super().perform_destroy(instance)


class ConceptFilterMixin:
    def get_concept_filter(self):
        return {"concept": False}

    def get_queryset(self):
        qs = super().get_queryset()

        if not hasattr(self, "action") or self.action != "list":
            return qs

        # show only non-concepts by default
        query_params = self.request.query_params or {}
        if "status" in query_params:
            return qs

        return qs.filter(**self.get_concept_filter())


class ConceptMixin(ConceptPublishMixin, ConceptDestroyMixin, ConceptFilterMixin):
    """ mixin for resources which have 'concept' field"""

    pass


class ZaakTypeConceptDestroyMixin(ConceptDestroyMixin):
    def get_concept(self, instance):
        return instance.zaaktype.concept

    def perform_destroy(self, instance):
        if not self.get_concept(instance):
            msg = _(
                "Objecten gerelateerd aan non-concept zaaktypen kunnen niet verwijderd worden."
            )
            raise ValidationError({"nonFieldErrors": msg}, code="non-concept-zaaktype")

        super().perform_destroy(instance)


class ZaakTypeConceptFilterMixin(ConceptFilterMixin):
    def get_concept_filter(self):
        return {"zaaktype__concept": False}


class ZaakTypeConceptMixin(ZaakTypeConceptDestroyMixin, ZaakTypeConceptFilterMixin):
    """
    mixin for resources which have FK or one-to-one relations with ZaakType objects,
    which support concept functionality
    """

    pass


class M2MConceptDestroyMixin:
    def perform_destroy(self, instance):
        for field_name in self.concept_related_fields:
            field = getattr(instance, field_name)
            related_non_concepts = field.filter(concept=False)
            if related_non_concepts.exists():
                msg = _(
                    f"Objects related to non-concept {field_name} can't be destroyed"
                )
                raise ValidationError(
                    {"nonFieldErrors": msg}, code="non-concept-relation"
                )

        super().perform_destroy(instance)
