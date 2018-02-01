from django.urls import reverse

from ...datamodel.tests.factories import InformatieObjectTypeFactory
from .base import APITestCase


class InformatieObjectTypeAPITests(APITestCase):
    def setUp(self):
        super().setUp()

        self.informatieobjecttype = InformatieObjectTypeFactory.create(maakt_deel_uit_van=self.catalogus)

        self.informatieobjecttype_list_url = reverse('api:informatieobjecttype-list', kwargs={
            'version': '1',
            'catalogus_pk': self.catalogus.pk,
        })

        self.informatieobjecttype_detail_url = reverse('api:informatieobjecttype-detail', kwargs={
            'version': '1',
            'catalogus_pk': self.catalogus.pk,
            'pk': self.informatieobjecttype.pk
        })

    def test_get_list(self):
        """Retrieve a list of `InformatieObjectType` objects."""
        response = self.api_client.get(self.informatieobjecttype_list_url)
        self.assertEqual(response.status_code, 200)

    def test_get_detail(self):
        """Retrieve the details of a single `InformatieObjectType` object."""
        response = self.api_client.get(self.informatieobjecttype_detail_url)
        self.assertEqual(response.status_code, 200)
