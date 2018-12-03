"""
Guarantee that the proper authorization amchinery is in place.
"""
import uuid

from rest_framework.test import APITestCase
from zds_schema.tests import AuthCheckMixin

from .utils import reverse


class ReadTests(AuthCheckMixin, APITestCase):

    def test_cannot_read_without_correct_scope(self):
        dummy_uuid = str(uuid.uuid4())
        urls = [
            # root
            reverse('catalogus-list'),
            reverse('catalogus-detail', kwargs={'uuid': dummy_uuid}),

            # nested one level
            reverse('zaaktype-list', kwargs={
                'catalogus_uuid': dummy_uuid
            }),
            reverse('zaaktype-detail', kwargs={
                'catalogus_uuid': dummy_uuid,
                'uuid': dummy_uuid,
            }),
            reverse('informatieobjecttype-list', kwargs={
                'catalogus_uuid': dummy_uuid
            }),
            reverse('informatieobjecttype-detail', kwargs={
                'catalogus_uuid': dummy_uuid,
                'uuid': dummy_uuid,
            }),
            reverse('besluittype-list', kwargs={
                'catalogus_uuid': dummy_uuid
            }),
            reverse('besluittype-detail', kwargs={
                'catalogus_uuid': dummy_uuid,
                'uuid': dummy_uuid,
            }),

            # nested two levels
            reverse('statustype-list', kwargs={
                'catalogus_uuid': dummy_uuid,
                'zaaktype_uuid': dummy_uuid,
            }),
            reverse('statustype-detail', kwargs={
                'catalogus_uuid': dummy_uuid,
                'zaaktype_uuid': dummy_uuid,
                'uuid': dummy_uuid,
            }),
            reverse('eigenschap-list', kwargs={
                'catalogus_uuid': dummy_uuid,
                'zaaktype_uuid': dummy_uuid,
            }),
            reverse('eigenschap-detail', kwargs={
                'catalogus_uuid': dummy_uuid,
                'zaaktype_uuid': dummy_uuid,
                'uuid': dummy_uuid,
            }),
            reverse('roltype-list', kwargs={
                'catalogus_uuid': dummy_uuid,
                'zaaktype_uuid': dummy_uuid,
            }),
            reverse('roltype-detail', kwargs={
                'catalogus_uuid': dummy_uuid,
                'zaaktype_uuid': dummy_uuid,
                'uuid': dummy_uuid,
            }),

        ]

        for url in urls:
            with self.subTest(url=url):
                self.assertForbidden(url, method='get')
