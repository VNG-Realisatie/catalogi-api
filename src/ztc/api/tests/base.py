from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from oauth2_provider.models import AccessToken

from ...datamodel.tests.factories import CatalogusFactory


class ClientAPITestMixin:
    def setUp(self):
        super().setUp()

        # Create a token without the whole authentication flow.
        self.token = AccessToken.objects.create(
            token='12345', expires=timezone.now() + timedelta(days=1), scope='write read')

        # Create a simple API client using our token and default JSON content type.
        self.api_client = self.client_class(
            content_type='application/json', AUTHORIZATION='Bearer {}'.format(self.token.token))


class CatalogusAPITestMixin:
    API_VERSION = '1'

    def setUp(self):
        super().setUp()

        self.catalogus = CatalogusFactory.create(domein='ABCDE', rsin='000000001')

        self.catalogus_list_url = reverse('api:catalogus-list', kwargs={'version': self.API_VERSION})
        self.catalogus_detail_url = reverse('api:catalogus-detail', kwargs={
            'version': self.API_VERSION, 'pk': self.catalogus.pk})


class APITestCase(ClientAPITestMixin, CatalogusAPITestMixin, TestCase):
    pass
