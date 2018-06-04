import json

from django.test import TestCase
from django.urls import reverse

from .base import ClientAPITestMixin


class DocumentationAPITests(ClientAPITestMixin, TestCase):
    """Section 2.6.3 of the DSO: API strategy"""

    def setUp(self):
        super().setUp()

        self.schema_url = reverse('api:api-schema', kwargs={'version': '1'})

    def test_schema_does_not_contain_flex_serializers(self):
        """
        If ``Serializer.Meta.ref_name`` is not explitely set, and ``drf-flex-fields`` is used, this causes the schema
        to have incorrect references.

        See: https://github.com/rsinger86/drf-flex-fields/issues/9
        """
        response = self.api_client.get('{}?format=openapi'.format(self.schema_url))
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content.decode('utf-8'))

        self.assertFalse('DynamicFieldsModel' in data)
