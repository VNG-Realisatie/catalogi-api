import warnings
from datetime import timedelta

from django.utils import timezone

from oauth2_provider.models import AccessToken
from rest_framework.test import APITestCase as _APITestCase
from zds_schema.tests import get_operation_url

from ...datamodel.tests.factories import CatalogusFactory


class ClientAPITestMixin:

    def setUp(self):
        super().setUp()

        # Create a token without the whole authentication flow.
        self.token = AccessToken.objects.create(
            token='12345',
            expires=timezone.now() + timedelta(days=1),
            scope='write read'
        )

        # Set up auth
        self.client.credentials(AUTHORIZATION='Bearer 12345')

    @property
    def api_client(self):
        warnings.warn("Use the built in `self.client` instead of `self.api_client`", DeprecationWarning)
        return self.client


class CatalogusAPITestMixin:
    API_VERSION = '1'

    def setUp(self):
        super().setUp()

        self.catalogus = CatalogusFactory.create(domein='ABCDE', rsin='000000001')

        self.catalogus_list_url = get_operation_url('catalogus_list')
        self.catalogus_detail_url = get_operation_url('catalogus_read', uuid=self.catalogus.uuid)


class APITestCase(ClientAPITestMixin, CatalogusAPITestMixin, _APITestCase):
    pass
