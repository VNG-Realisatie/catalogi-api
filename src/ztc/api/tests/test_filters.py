from rest_framework import status
from vng_api_common.tests import get_validation_errors, reverse

from ...datamodel.models import (
    BesluitType,
    Eigenschap,
    InformatieObjectType,
    ResultaatType,
    RolType,
    StatusType,
    ZaakInformatieobjectType,
    ZaakType,
)
from ...datamodel.tests.factories import (
    BesluitTypeFactory,
    EigenschapFactory,
    InformatieObjectTypeFactory,
    ResultaatTypeFactory,
    RolTypeFactory,
    StatusTypeFactory,
    ZaakInformatieobjectTypeFactory,
    ZaakTypeFactory,
)
from .base import APITestCase


class BesluitTypeFilterTests(APITestCase):
    heeft_alle_autorisaties = True

    def test_filter_by_invalid_url(self):
        for query_param in ["catalogus", "zaaktypen", "informatieobjecttypen"]:
            with self.subTest(query_param=query_param):
                response = self.client.get(reverse(BesluitType), {query_param: "bla"})

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

                error = get_validation_errors(response, query_param)
                self.assertEqual(error["code"], "invalid")

    def test_filter_by_valid_url_object_does_not_exist(self):
        besluittype = BesluitTypeFactory.create(concept=False)
        besluittype.zaaktypen.clear()
        besluittype.informatieobjecttypen.clear()
        for query_param in ["catalogus", "zaaktypen", "informatieobjecttypen"]:
            with self.subTest(query_param=query_param):
                response = self.client.get(
                    reverse(BesluitType), {query_param: "https://google.com"}
                )

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(
                    response.data,
                    {"count": 0, "next": None, "previous": None, "results": []},
                )


class EigenschapFilterTests(APITestCase):
    heeft_alle_autorisaties = True

    def test_filter_by_invalid_url(self):
        response = self.client.get(reverse(Eigenschap), {"zaaktype": "bla"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "zaaktype")
        self.assertEqual(error["code"], "invalid")

    def test_filter_by_valid_url_object_does_not_exist(self):
        EigenschapFactory.create(zaaktype__concept=False)
        response = self.client.get(
            reverse(Eigenschap), {"zaaktype": "https://google.com"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {"count": 0, "next": None, "previous": None, "results": []}
        )


class InformatieObjectTypeFilterTests(APITestCase):
    heeft_alle_autorisaties = True

    def test_filter_by_invalid_url(self):
        response = self.client.get(reverse(InformatieObjectType), {"catalogus": "bla"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "catalogus")
        self.assertEqual(error["code"], "invalid")

    def test_filter_by_valid_url_object_does_not_exist(self):
        informatieobjecttype = InformatieObjectTypeFactory.create(concept=False)
        informatieobjecttype.zaaktypen.clear()

        response = self.client.get(
            reverse(InformatieObjectType), {"catalogus": "https://google.com"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {"count": 0, "next": None, "previous": None, "results": []}
        )


class ResultaatTypeFilterTests(APITestCase):
    heeft_alle_autorisaties = True

    def test_filter_by_invalid_url(self):
        response = self.client.get(reverse(ResultaatType), {"zaaktype": "bla"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "zaaktype")
        self.assertEqual(error["code"], "invalid")

    def test_filter_by_valid_url_object_does_not_exist(self):
        ResultaatTypeFactory.create(zaaktype__concept=False)
        response = self.client.get(
            reverse(ResultaatType), {"zaaktype": "https://google.com"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {"count": 0, "next": None, "previous": None, "results": []}
        )


class RolTypeFilterTests(APITestCase):
    heeft_alle_autorisaties = True

    def test_filter_by_invalid_url(self):
        response = self.client.get(reverse(RolType), {"zaaktype": "bla"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "zaaktype")
        self.assertEqual(error["code"], "invalid")

    def test_filter_by_valid_url_object_does_not_exist(self):
        RolTypeFactory.create(zaaktype__concept=False)
        response = self.client.get(reverse(RolType), {"zaaktype": "https://google.com"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {"count": 0, "next": None, "previous": None, "results": []}
        )


class StatusTypeFilterTests(APITestCase):
    heeft_alle_autorisaties = True

    def test_filter_by_invalid_url(self):
        response = self.client.get(reverse(StatusType), {"zaaktype": "bla"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "zaaktype")
        self.assertEqual(error["code"], "invalid")

    def test_filter_by_valid_url_object_does_not_exist(self):
        StatusTypeFactory.create(zaaktype__concept=False)
        response = self.client.get(
            reverse(StatusType), {"zaaktype": "https://google.com"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {"count": 0, "next": None, "previous": None, "results": []}
        )


class ZaakInformatieobjectTypeFilterTests(APITestCase):
    heeft_alle_autorisaties = True

    def test_filter_by_invalid_url(self):
        for query_param in ["zaaktype", "informatieobjecttype"]:
            with self.subTest(query_param=query_param):
                response = self.client.get(
                    reverse(ZaakInformatieobjectType), {query_param: "bla"}
                )

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

                error = get_validation_errors(response, query_param)
                self.assertEqual(error["code"], "invalid")

    def test_filter_by_valid_url_object_does_not_exist(self):
        ZaakInformatieobjectTypeFactory.create(
            informatieobjecttype__concept=False, zaaktype__concept=False
        )
        for query_param in ["zaaktype", "informatieobjecttype"]:
            with self.subTest(query_param=query_param):
                response = self.client.get(
                    reverse(ZaakInformatieobjectType),
                    {query_param: "https://google.com"},
                )

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(
                    response.data,
                    {"count": 0, "next": None, "previous": None, "results": []},
                )


class ZaakTypeFilterTests(APITestCase):
    heeft_alle_autorisaties = True

    def test_filter_by_invalid_url(self):
        response = self.client.get(reverse(ZaakType), {"catalogus": "bla"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "catalogus")
        self.assertEqual(error["code"], "invalid")

    def test_filter_by_valid_url_object_does_not_exist(self):
        zaaktype = ZaakTypeFactory.create(concept=False)
        zaaktype.informatieobjecttypen.clear()

        response = self.client.get(
            reverse(ZaakType), {"catalogus": "https://google.com"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {"count": 0, "next": None, "previous": None, "results": []}
        )
