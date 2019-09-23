from django.utils.translation import ugettext_lazy as _

from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response


class ConceptPublishMixin:
    @swagger_auto_schema(request_body=no_body)
    @action(detail=True, methods=["post"])
    def publish(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.concept = False
        instance.save()

        serializer = self.get_serializer(instance)

        return Response(serializer.data)


class ConceptUpdateMixin:
    def get_concept(self, instance):
        return self.get_object().concept

    def perform_update(self, instance):
        if not self.get_concept(instance):
            msg = _("Alleen concepten kunnen worden bijgewerkt.")
            raise PermissionDenied(detail=msg)

        super().perform_update(instance)


class ConceptDestroyMixin:
    def get_concept(self, instance):
        return instance.concept

    def perform_destroy(self, instance):
        if not self.get_concept(instance):
            msg = _("Alleen concepten kunnen worden verwijderd.")
            raise PermissionDenied(detail=msg)

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


class ConceptMixin(
    ConceptPublishMixin, ConceptUpdateMixin, ConceptDestroyMixin, ConceptFilterMixin
):
    """ mixin for resources which have 'concept' field"""

    pass


class ZaakTypeConceptCreateMixin:
    def perform_create(self, serializer):
        zaaktype = serializer.validated_data["zaaktype"]
        if not zaaktype.concept:
            msg = _("Creating a related object to non-concept object is forbidden")
            raise PermissionDenied(detail=msg)

        super().perform_create(serializer)


class ZaakTypeConceptDestroyMixin(ConceptDestroyMixin):
    def get_concept(self, instance):
        return instance.zaaktype.concept


class ZaakTypeConceptFilterMixin(ConceptFilterMixin):
    def get_concept_filter(self):
        return {"zaaktype__concept": False}


class ZaakTypeConceptMixin(
    ZaakTypeConceptCreateMixin, ZaakTypeConceptDestroyMixin, ZaakTypeConceptFilterMixin
):
    """
    mixin for resources which have FK or one-to-one relations with ZaakType objects,
    which support concept functionality
    """

    pass


class M2MConceptCreateMixin:

    concept_related_fields = []

    def perform_create(self, serializer):
        for field_name in self.concept_related_fields:
            field = serializer.validated_data.get(field_name, [])
            for related_object in field:
                if not related_object.concept:
                    msg = _(
                        f"Relations to non-concept {field_name} object can't be created"
                    )
                    raise PermissionDenied(detail=msg)

        super().perform_create(serializer)


class M2MConceptUpdateMixin:
    def perform_update(self, instance):
        for field_name in self.concept_related_fields:
            field = getattr(self.get_object(), field_name)
            related_non_concepts = field.filter(concept=False)
            if related_non_concepts.exists():
                msg = _(f"Objects related to non-concept {field_name} can't be updated")
                raise PermissionDenied(detail=msg)

            # Validate that no new relations are created to resources with
            # non-concept status
            field_in_attrs = instance.validated_data.get(field_name)
            if field_in_attrs:
                for relation in field_in_attrs:
                    if not relation.concept:
                        msg = _(f"Objects can't be updated with a relation to non-concept {field_name}")
                        raise PermissionDenied(detail=msg)

        super().perform_update(instance)


class M2MConceptDestroyMixin:
    def perform_destroy(self, instance):
        for field_name in self.concept_related_fields:
            field = getattr(instance, field_name)
            related_non_concepts = field.filter(concept=False)
            if related_non_concepts.exists():
                msg = _(
                    f"Objects related to non-concept {field_name} can't be destroyed"
                )
                raise PermissionDenied(detail=msg)

        super().perform_destroy(instance)


class M2MConceptMixin(
    M2MConceptCreateMixin, M2MConceptUpdateMixin, M2MConceptDestroyMixin
):
    pass
