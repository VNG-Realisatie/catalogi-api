"""
Guarantee that the proper authorization amchinery is in place.
"""
from rest_framework.test import APITestCase
from zds_schema.tests import AuthCheckMixin

from .utils import reverse


class ReadTests(AuthCheckMixin, APITestCase):

    def test_cannot_read_without_correct_scope(self):
        urls = [
            # root
            reverse('catalogus-list'),
            reverse('catalogus-detail', kwargs={'uuid': 'dummy'}),

            # nested one level
            reverse('zaaktype-list', kwargs={
                'catalogus_uuid': 'dummy'
            }),
            reverse('zaaktype-detail', kwargs={
                'catalogus_uuid': 'dummy',
                'uuid': 'dummy',
            }),
            reverse('informatieobjecttype-list', kwargs={
                'catalogus_uuid': 'dummy'
            }),
            reverse('informatieobjecttype-detail', kwargs={
                'catalogus_uuid': 'dummy',
                'uuid': 'dummy',
            }),
            reverse('besluittype-list', kwargs={
                'catalogus_uuid': 'dummy'
            }),
            reverse('besluittype-detail', kwargs={
                'catalogus_uuid': 'dummy',
                'uuid': 'dummy',
            }),

            # nested two levels
            reverse('statustype-list', kwargs={
                'catalogus_uuid': 'dummy',
                'zaaktype_uuid': 'dummy',
            }),
            reverse('statustype-detail', kwargs={
                'catalogus_uuid': 'dummy',
                'zaaktype_uuid': 'dummy',
                'uuid': 'dummy',
            }),
            reverse('eigenschap-list', kwargs={
                'catalogus_uuid': 'dummy',
                'zaaktype_uuid': 'dummy',
            }),
            reverse('eigenschap-detail', kwargs={
                'catalogus_uuid': 'dummy',
                'zaaktype_uuid': 'dummy',
                'uuid': 'dummy',
            }),
            reverse('roltype-list', kwargs={
                'catalogus_uuid': 'dummy',
                'zaaktype_uuid': 'dummy',
            }),
            reverse('roltype-detail', kwargs={
                'catalogus_uuid': 'dummy',
                'zaaktype_uuid': 'dummy',
                'uuid': 'dummy',
            }),

        ]

        for url in urls:
            with self.subTest(url=url):
                self.assertForbidden(url, method='get')
