"""
Guarantee that the proper authorization amchinery is in place.
"""
from rest_framework import status
from rest_framework.test import APITestCase
from zds_schema.models import JWTSecret
from zds_schema.scopes import Scope
from zds_schema.tests import generate_jwt

from .utils import reverse


class AuthCheckMixin:

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        JWTSecret.objects.get_or_create(
            identifier='testsuite',
            defaults={'secret': 'letmein'}
        )

    def assertForbidden(self, url, method='get'):
        """
        Assert that an appropriate scope is required.
        """
        do_request = getattr(self.client, method)

        with self.subTest(case='JWT missing'):
            response = do_request(url)

            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        with self.subTest(case='Correct scope missing'):
            jwt = generate_jwt(scopes=[Scope('invalid.scope')])
            self.client.credentials(HTTP_AUTHORIZATION=jwt)

            response = do_request(url)

            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def assertForbiddenWithCorrectScope(
            self, url: str, scopes: list, method='get',
            request_kwargs=None, **extra_claims):

        do_request = getattr(self.client, method)
        request_kwargs = request_kwargs or {}

        jwt = generate_jwt(scopes=scopes, **extra_claims)
        self.client.credentials(HTTP_AUTHORIZATION=jwt)

        response = do_request(url, **request_kwargs)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


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
