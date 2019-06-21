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


class ZaakTypeDraftDestroyMixin(DraftDestroyMixin):
    def get_draft(self, instance):
        return instance.zaaktype.draft


class DraftMixin(DraftPublishMixin, DraftDestroyMixin):
    pass
