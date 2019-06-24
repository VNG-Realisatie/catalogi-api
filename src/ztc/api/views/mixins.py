from django.utils.translation import ugettext_lazy as _

from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response


class DraftPublishMixin:
    @swagger_auto_schema(
        request_body=no_body,
    )
    @action(detail=True, methods=['post'])
    def publish(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.draft = False
        instance.save()

        serializer = self.get_serializer(instance)

        return Response(serializer.data)


class DraftDestroyMixin:
    def get_draft(self, instance):
        return instance.draft

    def perform_destroy(self, instance):
        if not self.get_draft(instance):
            msg = _("Deleting a non-draft object is forbidden")
            raise PermissionDenied(detail=msg)

        super().perform_destroy(instance)


class DraftMixin(DraftPublishMixin,
                 DraftDestroyMixin):
    """ mixin for resources which have 'draft' field"""
    pass


class ZaakTypeDraftCreateMixin:
    def perform_create(self, serializer):
        zaaktype = serializer.validated_data['zaaktype']
        if not zaaktype.draft:
            msg = _("Creating a related object to non-draft object is forbidden")
            raise PermissionDenied(detail=msg)

        super().perform_create(serializer)


class ZaakTypeDraftDestroyMixin(DraftDestroyMixin):
    def get_draft(self, instance):
        return instance.zaaktype.draft


class ZaakTypeDraftMixin(ZaakTypeDraftCreateMixin,
                         ZaakTypeDraftDestroyMixin):
    """
    mixin for resources which have FK or one-to-one relations with ZaakType objects,
    which support draft functionality
    """
    pass


class M2MDraftCreateMixin:

    draft_related_fields = []

    def perform_create(self, serializer):
        for field_name in self.draft_related_fields:
            field = serializer.validated_data.get(field_name, [])
            for related_object in field:
                if not related_object.draft:
                    msg = _(f"Relations to a non-draft {field_name} object can't be created")
                    raise PermissionDenied(detail=msg)

        super().perform_create(serializer)
