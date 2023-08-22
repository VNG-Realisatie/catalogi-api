from functools import wraps
from typing import Union

from django.db import models
from django.utils.translation import ugettext_lazy as _

from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from vng_api_common.schema import COMMON_ERRORS
from vng_api_common.serializers import FoutSerializer, ValidatieFoutSerializer

from ..scopes import SCOPE_CATALOGI_FORCED_DELETE, SCOPE_CATALOGI_FORCED_WRITE
from ..utils.viewsets import extract_relevant_m2m


def swagger_publish_schema(viewset_cls):
    real_publish = viewset_cls.publish

    @extend_schema(
        request=None,
        responses={
            status.HTTP_200_OK: viewset_cls.serializer_class,
            status.HTTP_400_BAD_REQUEST: ValidatieFoutSerializer,
            status.HTTP_404_NOT_FOUND: FoutSerializer,
            **{exc.status_code: FoutSerializer for exc in COMMON_ERRORS},
        },
    )
    @wraps(real_publish)
    def _publish(*args, **kwargs):
        return real_publish(*args, **kwargs)

    return _publish


class ConceptPublishMixin:
    @action(detail=True, methods=["post"])
    def publish(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.concept = False
        instance.save()

        serializer = self.get_serializer(instance)

        return Response(serializer.data)


class ConceptDestroyMixin:
    message = _("Alleen concepten kunnen worden verwijderd.")
    code = "non-concept-object"

    def get_concept(self, instance):
        return instance.concept

    def perform_destroy(self, instance):
        forced_delete = self.request.jwt_auth.has_auth(
            scopes=SCOPE_CATALOGI_FORCED_DELETE
        )

        if not forced_delete:
            if not self.get_concept(instance):
                raise ValidationError({"nonFieldErrors": self.message}, code=self.code)

        super().perform_destroy(instance)


class ConceptFilterMixin:
    def get_concept_filter(self) -> Union[dict, models.Q]:
        return {"concept": False}

    def get_queryset(self):
        qs = super().get_queryset()

        if not hasattr(self, "action") or self.action != "list":
            return qs

        # show only non-concepts by default
        query_params = self.request.query_params or {}
        if "status" in query_params:
            return qs

        filters = self.get_concept_filter()
        if not isinstance(filters, models.Q):
            filters = models.Q(**filters)
        return qs.filter(filters)


class ConceptMixin(ConceptPublishMixin, ConceptDestroyMixin, ConceptFilterMixin):
    """mixin for resources which have 'concept' field"""

    pass


class ForcedCreateUpdateMixin(viewsets.GenericViewSet):
    def get_serializer_context(self):
        context = super().get_serializer_context()
        allow_action_with_force = False
        if self.action in ["update", "partial_update", "create"]:
            if self.request.jwt_auth.has_auth(
                scopes=SCOPE_CATALOGI_FORCED_WRITE,
            ):
                allow_action_with_force = True

        context.update({"allow_action_with_force": allow_action_with_force})
        return context


class ZaakTypeConceptDestroyMixin(ConceptDestroyMixin):
    message = _(
        "Objecten gerelateerd aan non-concept zaaktypen kunnen niet verwijderd worden."
    )
    code = "non-concept-zaaktype"

    def get_concept(self, instance):
        return instance.zaaktype.concept


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
        forced_delete = self.request.jwt_auth.has_auth(
            scopes=SCOPE_CATALOGI_FORCED_DELETE
        )

        if not forced_delete:
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
