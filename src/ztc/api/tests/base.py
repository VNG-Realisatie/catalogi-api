from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from oauth2_provider.models import AccessToken

from ...datamodel.models import BesluitType, Catalogus


class ClientAPITestMixin(object):
    def setUp(self):
        super().setUp()

        # Create a token without the whole authentication flow.
        self.token = AccessToken.objects.create(
            token='12345', expires=timezone.now() + timedelta(days=1), scope='write read')

        # Create a simple API client using our token and default JSON content type.
        self.api_client = self.client_class(
            content_type='application/json', AUTHORIZATION='Bearer {}'.format(self.token.token))


class CatalogusAPITestMixin(object):
    def setUp(self):
        super().setUp()

        self.catalogus = Catalogus.objects.create(domein='ABCDE', rsin='000012345')

        self.list_url = reverse('api:catalogus-list', kwargs={'version': '1'})
        self.detail_url = reverse('api:catalogus-detail', kwargs={'version': '1', 'pk': self.catalogus.pk})

        self.besluittype = BesluitType.objects.create(
            maakt_deel_uit_van=self.catalogus, reactietermijn=14, publicatie_indicatie='J')


class APITestCase(ClientAPITestMixin, CatalogusAPITestMixin, TestCase):
    pass
