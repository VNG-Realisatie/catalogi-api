"""
Test that the caching mechanisms are in place.
"""
from rest_framework import status
from rest_framework.test import APITestCase, APITransactionTestCase
from vng_api_common.caching import calculate_etag
from vng_api_common.tests import CacheMixin, JWTAuthMixin, generate_jwt_auth, reverse
from vng_api_common.tests.schema import get_spec

from ztc.datamodel.tests.factories import (
    BesluitTypeFactory,
    CatalogusFactory,
    EigenschapFactory,
    InformatieObjectTypeFactory,
    ZaakInformatieobjectTypeFactory,
    ResultaatTypeFactory,
    RolTypeFactory,
    StatusTypeFactory,
    ZaakTypeFactory,
)


class BesluitTypeCacheTests(CacheMixin, JWTAuthMixin, APITestCase):
    heeft_alle_autorisaties = True

    def test_besluittype_get_cache_header(self):
        besluittype = BesluitTypeFactory.create()

        response = self.client.get(reverse(besluittype))

        self.assertHasETag(response)

    def test_besluittype_head_cache_header(self):
        besluittype = BesluitTypeFactory.create()

        self.assertHeadHasETag(reverse(besluittype))

    def test_head_in_apischema(self):
        spec = get_spec()

        endpoint = spec["paths"]["/besluittypen/{uuid}"]

        self.assertIn("head", endpoint)

    def test_conditional_get_304(self):
        besluittype = BesluitTypeFactory.create(with_etag=True)
        response = self.client.get(
            reverse(besluittype), HTTP_IF_NONE_MATCH=f'"{besluittype._etag}"'
        )

        self.assertEqual(response.status_code, status.HTTP_304_NOT_MODIFIED)

    def test_conditional_get_stale(self):
        besluittype = BesluitTypeFactory.create(with_etag=True)

        response = self.client.get(
            reverse(besluittype), HTTP_IF_NONE_MATCH=f'"not-an-md5"'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BesluitTypeCacheTransactionTests(JWTAuthMixin, APITransactionTestCase):
    heeft_alle_autorisaties = True

    def setUp(self):
        super().setUp()
        self._create_credentials(
            self.client_id,
            self.secret,
            self.heeft_alle_autorisaties,
            self.max_vertrouwelijkheidaanduiding,
        )

    def test_invalidate_etag_after_change(self):
        """
        Because changes are made to the besluittype, a code 200 should be
        returned
        """
        besluittype = BesluitTypeFactory.create(omschrijving="bla", with_etag=True)
        besluittype._etag = calculate_etag(besluittype)
        besluittype.save(update_fields=["_etag"])
        etag = besluittype._etag

        besluittype.omschrijving = "same"
        besluittype.save()

        response = self.client.get(reverse(besluittype), HTTP_IF_NONE_MATCH=f'"{etag}"')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_changes_gives_304(self):
        """
        Because no changes are made to the besluittype, a code 304 should be
        returned
        """
        besluittype = BesluitTypeFactory.create(omschrijving="bla")
        besluittype._etag = calculate_etag(besluittype)
        besluittype.save(update_fields=["_etag"])
        etag = besluittype._etag

        response = self.client.get(reverse(besluittype), HTTP_IF_NONE_MATCH=f'"{etag}"')
        self.assertEqual(response.status_code, status.HTTP_304_NOT_MODIFIED)


class CatalogusCacheTests(CacheMixin, JWTAuthMixin, APITestCase):
    heeft_alle_autorisaties = True

    def test_catalogus_get_cache_header(self):
        catalogus = CatalogusFactory.create()

        response = self.client.get(reverse(catalogus))

        self.assertHasETag(response)

    def test_catalogus_head_cache_header(self):
        catalogus = CatalogusFactory.create()

        self.assertHeadHasETag(reverse(catalogus))

    def test_head_in_apischema(self):
        spec = get_spec()

        endpoint = spec["paths"]["/catalogussen/{uuid}"]

        self.assertIn("head", endpoint)

    def test_conditional_get_304(self):
        catalogus = CatalogusFactory.create(with_etag=True)
        response = self.client.get(
            reverse(catalogus), HTTP_IF_NONE_MATCH=f'"{catalogus._etag}"'
        )

        self.assertEqual(response.status_code, status.HTTP_304_NOT_MODIFIED)

    def test_conditional_get_stale(self):
        catalogus = CatalogusFactory.create(with_etag=True)

        response = self.client.get(
            reverse(catalogus), HTTP_IF_NONE_MATCH=f'"not-an-md5"'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CatalogusCacheTransactionTests(JWTAuthMixin, APITransactionTestCase):
    heeft_alle_autorisaties = True

    def setUp(self):
        super().setUp()
        self._create_credentials(
            self.client_id,
            self.secret,
            self.heeft_alle_autorisaties,
            self.max_vertrouwelijkheidaanduiding,
        )

    def test_invalidate_etag_after_change(self):
        """
        Because changes are made to the catalogus, a code 200 should be
        returned
        """
        catalogus = CatalogusFactory.create(domein="bla", with_etag=True)
        catalogus._etag = calculate_etag(catalogus)
        catalogus.save(update_fields=["_etag"])
        etag = catalogus._etag

        catalogus.domein = "same"
        catalogus.save()

        response = self.client.get(reverse(catalogus), HTTP_IF_NONE_MATCH=f'"{etag}"')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_changes_gives_304(self):
        """
        Because no changes are made to the catalogus, a code 304 should be
        returned
        """
        catalogus = CatalogusFactory.create(domein="bla")
        catalogus._etag = calculate_etag(catalogus)
        catalogus.save(update_fields=["_etag"])
        etag = catalogus._etag

        response = self.client.get(reverse(catalogus), HTTP_IF_NONE_MATCH=f'"{etag}"')
        self.assertEqual(response.status_code, status.HTTP_304_NOT_MODIFIED)


class EigenschapCacheTests(CacheMixin, JWTAuthMixin, APITestCase):
    heeft_alle_autorisaties = True

    def test_eigenschap_get_cache_header(self):
        eigenschap = EigenschapFactory.create()

        response = self.client.get(reverse(eigenschap))

        self.assertHasETag(response)

    def test_eigenschap_head_cache_header(self):
        eigenschap = EigenschapFactory.create()

        self.assertHeadHasETag(reverse(eigenschap))

    def test_head_in_apischema(self):
        spec = get_spec()

        endpoint = spec["paths"]["/eigenschappen/{uuid}"]

        self.assertIn("head", endpoint)

    def test_conditional_get_304(self):
        eigenschap = EigenschapFactory.create(with_etag=True)
        response = self.client.get(
            reverse(eigenschap), HTTP_IF_NONE_MATCH=f'"{eigenschap._etag}"'
        )

        self.assertEqual(response.status_code, status.HTTP_304_NOT_MODIFIED)

    def test_conditional_get_stale(self):
        eigenschap = EigenschapFactory.create(with_etag=True)

        response = self.client.get(
            reverse(eigenschap), HTTP_IF_NONE_MATCH=f'"not-an-md5"'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class EigenschapCacheTransactionTests(JWTAuthMixin, APITransactionTestCase):
    heeft_alle_autorisaties = True

    def setUp(self):
        super().setUp()
        self._create_credentials(
            self.client_id,
            self.secret,
            self.heeft_alle_autorisaties,
            self.max_vertrouwelijkheidaanduiding,
        )

    def test_invalidate_etag_after_change(self):
        """
        Because changes are made to the eigenschap, a code 200 should be
        returned
        """
        eigenschap = EigenschapFactory.create(toelichting="bla", with_etag=True)
        eigenschap._etag = calculate_etag(eigenschap)
        eigenschap.save(update_fields=["_etag"])
        etag = eigenschap._etag

        eigenschap.toelichting = "same"
        eigenschap.save()

        response = self.client.get(reverse(eigenschap), HTTP_IF_NONE_MATCH=f'"{etag}"')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_changes_gives_304(self):
        """
        Because no changes are made to the eigenschap, a code 304 should be
        returned
        """
        eigenschap = EigenschapFactory.create(toelichting="bla")
        eigenschap._etag = calculate_etag(eigenschap)
        eigenschap.save(update_fields=["_etag"])
        etag = eigenschap._etag

        response = self.client.get(reverse(eigenschap), HTTP_IF_NONE_MATCH=f'"{etag}"')
        self.assertEqual(response.status_code, status.HTTP_304_NOT_MODIFIED)


class InformatieObjectTypeCacheTests(CacheMixin, JWTAuthMixin, APITestCase):
    heeft_alle_autorisaties = True

    def test_informatieobjecttype_get_cache_header(self):
        informatieobjecttype = InformatieObjectTypeFactory.create()

        response = self.client.get(reverse(informatieobjecttype))

        self.assertHasETag(response)

    def test_informatieobjecttype_head_cache_header(self):
        informatieobjecttype = InformatieObjectTypeFactory.create()

        self.assertHeadHasETag(reverse(informatieobjecttype))

    def test_head_in_apischema(self):
        spec = get_spec()

        endpoint = spec["paths"]["/informatieobjecttypen/{uuid}"]

        self.assertIn("head", endpoint)

    def test_conditional_get_304(self):
        informatieobjecttype = InformatieObjectTypeFactory.create(with_etag=True)
        response = self.client.get(
            reverse(informatieobjecttype),
            HTTP_IF_NONE_MATCH=f'"{informatieobjecttype._etag}"',
        )

        self.assertEqual(response.status_code, status.HTTP_304_NOT_MODIFIED)

    def test_conditional_get_stale(self):
        informatieobjecttype = InformatieObjectTypeFactory.create(with_etag=True)

        response = self.client.get(
            reverse(informatieobjecttype), HTTP_IF_NONE_MATCH=f'"not-an-md5"'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class InformatieObjectTypeCacheTransactionTests(JWTAuthMixin, APITransactionTestCase):
    heeft_alle_autorisaties = True

    def setUp(self):
        super().setUp()
        self._create_credentials(
            self.client_id,
            self.secret,
            self.heeft_alle_autorisaties,
            self.max_vertrouwelijkheidaanduiding,
        )

    def test_invalidate_etag_after_change(self):
        """
        Because changes are made to the informatieobjecttype, a code 200 should be
        returned
        """
        informatieobjecttype = InformatieObjectTypeFactory.create(
            omschrijving="bla", with_etag=True
        )
        informatieobjecttype._etag = calculate_etag(informatieobjecttype)
        informatieobjecttype.save(update_fields=["_etag"])
        etag = informatieobjecttype._etag

        informatieobjecttype.omschrijving = "same"
        informatieobjecttype.save()

        response = self.client.get(
            reverse(informatieobjecttype), HTTP_IF_NONE_MATCH=f'"{etag}"'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_changes_gives_304(self):
        """
        Because no changes are made to the informatieobjecttype, a code 304 should be
        returned
        """
        informatieobjecttype = InformatieObjectTypeFactory.create(omschrijving="bla")
        informatieobjecttype._etag = calculate_etag(informatieobjecttype)
        informatieobjecttype.save(update_fields=["_etag"])
        etag = informatieobjecttype._etag

        response = self.client.get(
            reverse(informatieobjecttype), HTTP_IF_NONE_MATCH=f'"{etag}"'
        )
        self.assertEqual(response.status_code, status.HTTP_304_NOT_MODIFIED)


class ResultaatTypeCacheTests(CacheMixin, JWTAuthMixin, APITestCase):
    heeft_alle_autorisaties = True

    def test_resultaattype_get_cache_header(self):
        resultaattype = ResultaatTypeFactory.create()

        response = self.client.get(reverse(resultaattype))

        self.assertHasETag(response)

    def test_resultaattype_head_cache_header(self):
        resultaattype = ResultaatTypeFactory.create()

        self.assertHeadHasETag(reverse(resultaattype))

    def test_head_in_apischema(self):
        spec = get_spec()

        endpoint = spec["paths"]["/resultaattypen/{uuid}"]

        self.assertIn("head", endpoint)

    def test_conditional_get_304(self):
        resultaattype = ResultaatTypeFactory.create(with_etag=True)
        response = self.client.get(
            reverse(resultaattype), HTTP_IF_NONE_MATCH=f'"{resultaattype._etag}"'
        )

        self.assertEqual(response.status_code, status.HTTP_304_NOT_MODIFIED)

    def test_conditional_get_stale(self):
        resultaattype = ResultaatTypeFactory.create(with_etag=True)

        response = self.client.get(
            reverse(resultaattype), HTTP_IF_NONE_MATCH=f'"not-an-md5"'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ResultaatTypeCacheTransactionTests(JWTAuthMixin, APITransactionTestCase):
    heeft_alle_autorisaties = True

    def setUp(self):
        super().setUp()
        self._create_credentials(
            self.client_id,
            self.secret,
            self.heeft_alle_autorisaties,
            self.max_vertrouwelijkheidaanduiding,
        )

    def test_invalidate_etag_after_change(self):
        """
        Because changes are made to the resultaattype, a code 200 should be
        returned
        """
        resultaattype = ResultaatTypeFactory.create(omschrijving="bla", with_etag=True)
        resultaattype._etag = calculate_etag(resultaattype)
        resultaattype.save(update_fields=["_etag"])
        etag = resultaattype._etag

        resultaattype.omschrijving = "same"
        resultaattype.save()

        response = self.client.get(
            reverse(resultaattype), HTTP_IF_NONE_MATCH=f'"{etag}"'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_changes_gives_304(self):
        """
        Because no changes are made to the resultaattype, a code 304 should be
        returned
        """
        resultaattype = ResultaatTypeFactory.create(omschrijving="bla")
        resultaattype._etag = calculate_etag(resultaattype)
        resultaattype.save(update_fields=["_etag"])
        etag = resultaattype._etag

        response = self.client.get(
            reverse(resultaattype), HTTP_IF_NONE_MATCH=f'"{etag}"'
        )
        self.assertEqual(response.status_code, status.HTTP_304_NOT_MODIFIED)


class RolTypeCacheTests(CacheMixin, JWTAuthMixin, APITestCase):
    heeft_alle_autorisaties = True

    def test_roltype_get_cache_header(self):
        roltype = RolTypeFactory.create()

        response = self.client.get(reverse(roltype))

        self.assertHasETag(response)

    def test_roltype_head_cache_header(self):
        roltype = RolTypeFactory.create()

        self.assertHeadHasETag(reverse(roltype))

    def test_head_in_apischema(self):
        spec = get_spec()

        endpoint = spec["paths"]["/roltypen/{uuid}"]

        self.assertIn("head", endpoint)

    def test_conditional_get_304(self):
        roltype = RolTypeFactory.create(with_etag=True)
        response = self.client.get(
            reverse(roltype), HTTP_IF_NONE_MATCH=f'"{roltype._etag}"'
        )

        self.assertEqual(response.status_code, status.HTTP_304_NOT_MODIFIED)

    def test_conditional_get_stale(self):
        roltype = RolTypeFactory.create(with_etag=True)

        response = self.client.get(reverse(roltype), HTTP_IF_NONE_MATCH=f'"not-an-md5"')

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RolTypeCacheTransactionTests(JWTAuthMixin, APITransactionTestCase):
    heeft_alle_autorisaties = True

    def setUp(self):
        super().setUp()
        self._create_credentials(
            self.client_id,
            self.secret,
            self.heeft_alle_autorisaties,
            self.max_vertrouwelijkheidaanduiding,
        )

    def test_invalidate_etag_after_change(self):
        """
        Because changes are made to the roltype, a code 200 should be
        returned
        """
        roltype = RolTypeFactory.create(omschrijving="bla", with_etag=True)
        roltype._etag = calculate_etag(roltype)
        roltype.save(update_fields=["_etag"])
        etag = roltype._etag

        roltype.omschrijving = "same"
        roltype.save()

        response = self.client.get(reverse(roltype), HTTP_IF_NONE_MATCH=f'"{etag}"')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_changes_gives_304(self):
        """
        Because no changes are made to the roltype, a code 304 should be
        returned
        """
        roltype = RolTypeFactory.create(omschrijving="bla")
        roltype._etag = calculate_etag(roltype)
        roltype.save(update_fields=["_etag"])
        etag = roltype._etag

        response = self.client.get(reverse(roltype), HTTP_IF_NONE_MATCH=f'"{etag}"')
        self.assertEqual(response.status_code, status.HTTP_304_NOT_MODIFIED)


class StatusTypeCacheTests(CacheMixin, JWTAuthMixin, APITestCase):
    heeft_alle_autorisaties = True

    def test_statustype_get_cache_header(self):
        statustype = StatusTypeFactory.create()

        response = self.client.get(reverse(statustype))

        self.assertHasETag(response)

    def test_statustype_head_cache_header(self):
        statustype = StatusTypeFactory.create()

        self.assertHeadHasETag(reverse(statustype))

    def test_head_in_apischema(self):
        spec = get_spec()

        endpoint = spec["paths"]["/statustypen/{uuid}"]

        self.assertIn("head", endpoint)

    def test_conditional_get_304(self):
        statustype = StatusTypeFactory.create(with_etag=True)
        response = self.client.get(
            reverse(statustype), HTTP_IF_NONE_MATCH=f'"{statustype._etag}"'
        )

        self.assertEqual(response.status_code, status.HTTP_304_NOT_MODIFIED)

    def test_conditional_get_stale(self):
        statustype = StatusTypeFactory.create(with_etag=True)

        response = self.client.get(
            reverse(statustype), HTTP_IF_NONE_MATCH=f'"not-an-md5"'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class StatusTypeCacheTransactionTests(JWTAuthMixin, APITransactionTestCase):
    heeft_alle_autorisaties = True

    def setUp(self):
        super().setUp()
        self._create_credentials(
            self.client_id,
            self.secret,
            self.heeft_alle_autorisaties,
            self.max_vertrouwelijkheidaanduiding,
        )

    def test_invalidate_etag_after_change(self):
        """
        Because changes are made to the statustype, a code 200 should be
        returned
        """
        statustype = StatusTypeFactory.create(statustekst="bla", with_etag=True)
        statustype._etag = calculate_etag(statustype)
        statustype.save(update_fields=["_etag"])
        etag = statustype._etag

        statustype.statustekst = "same"
        statustype.save()

        response = self.client.get(reverse(statustype), HTTP_IF_NONE_MATCH=f'"{etag}"')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_changes_gives_304(self):
        """
        Because no changes are made to the statustype, a code 304 should be
        returned
        """
        statustype = StatusTypeFactory.create(statustekst="bla")
        statustype._etag = calculate_etag(statustype)
        statustype.save(update_fields=["_etag"])
        etag = statustype._etag

        response = self.client.get(reverse(statustype), HTTP_IF_NONE_MATCH=f'"{etag}"')
        self.assertEqual(response.status_code, status.HTTP_304_NOT_MODIFIED)


class ZaakInformatieobjectTypeCacheTests(CacheMixin, JWTAuthMixin, APITestCase):
    heeft_alle_autorisaties = True

    def test_zaakinformatieobjecttype_get_cache_header(self):
        zaakinformatieobjecttype = ZaakInformatieobjectTypeFactory.create()

        response = self.client.get(reverse(zaakinformatieobjecttype))

        self.assertHasETag(response)

    def test_zaakinformatieobjecttype_head_cache_header(self):
        zaakinformatieobjecttype = ZaakInformatieobjectTypeFactory.create()

        self.assertHeadHasETag(reverse(zaakinformatieobjecttype))

    def test_head_in_apischema(self):
        spec = get_spec()

        endpoint = spec["paths"]["/zaaktype-informatieobjecttypen/{uuid}"]

        self.assertIn("head", endpoint)

    def test_conditional_get_304(self):
        zaakinformatieobjecttype = ZaakInformatieobjectTypeFactory.create(
            with_etag=True
        )
        response = self.client.get(
            reverse(zaakinformatieobjecttype),
            HTTP_IF_NONE_MATCH=f'"{zaakinformatieobjecttype._etag}"',
        )

        self.assertEqual(response.status_code, status.HTTP_304_NOT_MODIFIED)

    def test_conditional_get_stale(self):
        zaakinformatieobjecttype = ZaakInformatieobjectTypeFactory.create(
            with_etag=True
        )

        response = self.client.get(
            reverse(zaakinformatieobjecttype), HTTP_IF_NONE_MATCH=f'"not-an-md5"'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ZaakInformatieobjectTypeCacheTransactionTests(
    JWTAuthMixin, APITransactionTestCase
):
    heeft_alle_autorisaties = True

    def setUp(self):
        super().setUp()
        self._create_credentials(
            self.client_id,
            self.secret,
            self.heeft_alle_autorisaties,
            self.max_vertrouwelijkheidaanduiding,
        )

    def test_invalidate_etag_after_change(self):
        """
        Because changes are made to the zaakinformatieobjecttype, a code 200 should be
        returned
        """
        zaakinformatieobjecttype = ZaakInformatieobjectTypeFactory.create(
            volgnummer=1, with_etag=True
        )
        zaakinformatieobjecttype._etag = calculate_etag(zaakinformatieobjecttype)
        zaakinformatieobjecttype.save(update_fields=["_etag"])
        etag = zaakinformatieobjecttype._etag

        zaakinformatieobjecttype.volgnummer = 2
        zaakinformatieobjecttype.save()

        response = self.client.get(
            reverse(zaakinformatieobjecttype), HTTP_IF_NONE_MATCH=f'"{etag}"'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_changes_gives_304(self):
        """
        Because no changes are made to the zaakinformatieobjecttype, a code 304 should be
        returned
        """
        zaakinformatieobjecttype = ZaakInformatieobjectTypeFactory.create(volgnummer=1)
        zaakinformatieobjecttype._etag = calculate_etag(zaakinformatieobjecttype)
        zaakinformatieobjecttype.save(update_fields=["_etag"])
        etag = zaakinformatieobjecttype._etag

        response = self.client.get(
            reverse(zaakinformatieobjecttype), HTTP_IF_NONE_MATCH=f'"{etag}"'
        )
        self.assertEqual(response.status_code, status.HTTP_304_NOT_MODIFIED)


class ZaakTypeCacheTests(CacheMixin, JWTAuthMixin, APITestCase):
    heeft_alle_autorisaties = True

    def test_zaaktype_get_cache_header(self):
        zaaktype = ZaakTypeFactory.create()

        response = self.client.get(reverse(zaaktype))

        self.assertHasETag(response)

    def test_zaaktype_head_cache_header(self):
        zaaktype = ZaakTypeFactory.create()

        self.assertHeadHasETag(reverse(zaaktype))

    def test_head_in_apischema(self):
        spec = get_spec()

        endpoint = spec["paths"]["/zaaktypen/{uuid}"]

        self.assertIn("head", endpoint)

    def test_conditional_get_304(self):
        zaaktype = ZaakTypeFactory.create(with_etag=True)
        response = self.client.get(
            reverse(zaaktype), HTTP_IF_NONE_MATCH=f'"{zaaktype._etag}"'
        )

        self.assertEqual(response.status_code, status.HTTP_304_NOT_MODIFIED)

    def test_conditional_get_stale(self):
        zaaktype = ZaakTypeFactory.create(with_etag=True)

        response = self.client.get(
            reverse(zaaktype), HTTP_IF_NONE_MATCH=f'"not-an-md5"'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ZaakTypeCacheTransactionTests(JWTAuthMixin, APITransactionTestCase):
    heeft_alle_autorisaties = True

    def setUp(self):
        super().setUp()
        self._create_credentials(
            self.client_id,
            self.secret,
            self.heeft_alle_autorisaties,
            self.max_vertrouwelijkheidaanduiding,
        )

    def test_invalidate_etag_after_change(self):
        """
        Because changes are made to the zaaktype, a code 200 should be
        returned
        """
        zaaktype = ZaakTypeFactory.create(toelichting="bla")
        zaaktype._etag = calculate_etag(zaaktype)
        zaaktype.save(update_fields=["_etag"])
        etag = zaaktype._etag

        zaaktype.toelichting = "same"
        zaaktype.save()

        response = self.client.get(reverse(zaaktype), HTTP_IF_NONE_MATCH=f'"{etag}"')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_changes_gives_304(self):
        """
        Because changes are made to the zaaktype, a code 200 should be
        returned
        """
        zaaktype = ZaakTypeFactory.create(toelichting="bla")
        zaaktype._etag = calculate_etag(zaaktype)
        zaaktype.save(update_fields=["_etag"])
        etag = zaaktype._etag

        response = self.client.get(reverse(zaaktype), HTTP_IF_NONE_MATCH=f'"{etag}"')
        self.assertEqual(response.status_code, status.HTTP_304_NOT_MODIFIED)


class M2MRelationCachingTests(JWTAuthMixin, APITransactionTestCase):
    heeft_alle_autorisaties = True

    def setUp(self):
        super().setUp()
        self._create_credentials(
            self.client_id,
            self.secret,
            self.heeft_alle_autorisaties,
            self.max_vertrouwelijkheidaanduiding,
        )

    def test_changing_besluittype_zaaktype_m2m_invalidates_both_etags(self):
        """
        Changing the M2M should modify both resources, resulting in 200 for
        when both resources are retrieved
        """
        besluittype = BesluitTypeFactory.create()
        besluittype._etag = calculate_etag(besluittype)
        besluittype.save(update_fields=["_etag"])
        besluittype_etag = besluittype._etag

        zaaktype = ZaakTypeFactory.create()
        zaaktype._etag = calculate_etag(zaaktype)
        zaaktype.save(update_fields=["_etag"])
        zaaktype_etag = zaaktype._etag

        besluittype.zaaktypes.set([zaaktype])
        besluittype.save()

        response = self.client.get(
            reverse(besluittype), HTTP_IF_NONE_MATCH=f'"{besluittype_etag}"'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(
            reverse(zaaktype), HTTP_IF_NONE_MATCH=f'"{zaaktype_etag}"'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_changing_besluittype_informatieobjecttype_m2m_invalidates_both_etags(self):
        """
        Changing the M2M should modify both resources, resulting in 200 for
        when both resources are retrieved
        """
        besluittype = BesluitTypeFactory.create()
        besluittype._etag = calculate_etag(besluittype)
        besluittype.save(update_fields=["_etag"])
        besluittype_etag = besluittype._etag

        zaaktype = ZaakTypeFactory.create()
        zaaktype._etag = calculate_etag(zaaktype)
        zaaktype.save(update_fields=["_etag"])
        zaaktype_etag = zaaktype._etag

        besluittype.zaaktypes.set([zaaktype])
        besluittype.save()

        response = self.client.get(
            reverse(besluittype), HTTP_IF_NONE_MATCH=f'"{besluittype_etag}"'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(
            reverse(zaaktype), HTTP_IF_NONE_MATCH=f'"{zaaktype_etag}"'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
