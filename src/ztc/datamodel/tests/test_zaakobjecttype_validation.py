from datetime import date
from uuid import uuid4

from django.test import TestCase
from django.utils.translation import gettext as _

from ztc.datamodel.admin.forms import ZaakObjectTypeForm
from ztc.datamodel.tests.factories.catalogus import CatalogusFactory
from ztc.datamodel.tests.factories.zaakobjecttype import ZaakObjectTypeFactory
from ztc.datamodel.tests.factories.zaken import ZaakTypeFactory


class ZaaktypeValidationTests(TestCase):
    """
    Test the validation on ZaakObjectType
    """

    def test_create_datum_einde_geldigheid_validation(self):
        catalogus = CatalogusFactory()
        zaakobjecttype = ZaakObjectTypeFactory.stub(
            uuid=uuid4(),
            catalogus=catalogus,
            zaaktype=ZaakTypeFactory(catalogus=catalogus),
        )

        form = ZaakObjectTypeForm(
            data={
                "uuid": str(zaakobjecttype.uuid),
                "ander_objecttype": zaakobjecttype.ander_objecttype,
                "objecttype": zaakobjecttype.objecttype,
                "relatie_omschrijving": zaakobjecttype.relatie_omschrijving,
                "zaaktype": zaakobjecttype.zaaktype.pk,
                "catalogus": zaakobjecttype.catalogus.pk,
                "datum_begin_geldigheid": date(2021, 2, 1),
                "datum_einde_geldigheid": date(2021, 1, 1),
            }
        )

        self.assertFalse(form.is_valid())

        error = form.errors.as_data()["__all__"][0]
        self.assertEqual(
            error.message,
            _(
                "Datum einde geldigheid is gelijk aan of gelegen na de datum zoals opgenomen "
                "onder Datum begin geldigheid."
            ),
        )

    def test_update_datum_begin_geldigheid(self):
        catalogus = CatalogusFactory()
        zaakobjecttype = ZaakObjectTypeFactory(
            uuid=uuid4(),
            catalogus=catalogus,
            zaaktype=ZaakTypeFactory(catalogus=catalogus),
        )

        form = ZaakObjectTypeForm(
            data={
                "uuid": str(zaakobjecttype.uuid),
                "ander_objecttype": zaakobjecttype.ander_objecttype,
                "objecttype": zaakobjecttype.objecttype,
                "relatie_omschrijving": zaakobjecttype.relatie_omschrijving,
                "zaaktype": zaakobjecttype.zaaktype.pk,
                "catalogus": zaakobjecttype.catalogus.pk,
                "datum_begin_geldigheid": date(2021, 2, 1),
                "datum_einde_geldigheid": date(2021, 1, 1),
            },
            instance=zaakobjecttype,
        )

        self.assertFalse(form.is_valid())

        error = form.errors.as_data()["__all__"][0]
        self.assertEqual(
            error.message,
            _(
                "Datum einde geldigheid is gelijk aan of gelegen na de datum zoals opgenomen "
                "onder Datum begin geldigheid."
            ),
        )

    def test_create_non_concept_zaaktype(self):
        catalogus = CatalogusFactory()
        zaakobjecttype = ZaakObjectTypeFactory.stub(
            uuid=uuid4(),
            catalogus=catalogus,
            zaaktype=ZaakTypeFactory(catalogus=catalogus, concept=False),
        )

        form = ZaakObjectTypeForm(
            data={
                "uuid": str(zaakobjecttype.uuid),
                "ander_objecttype": zaakobjecttype.ander_objecttype,
                "objecttype": zaakobjecttype.objecttype,
                "relatie_omschrijving": zaakobjecttype.relatie_omschrijving,
                "zaaktype": zaakobjecttype.zaaktype.pk,
                "catalogus": zaakobjecttype.catalogus.pk,
                "datum_begin_geldigheid": date(2021, 1, 1),
            }
        )

        self.assertFalse(form.is_valid())

        error = form.errors.as_data()["__all__"][0]
        self.assertEqual(
            error.message,
            _("Objects related to non-concept objects can't be updated or created."),
        )

    def test_update_non_concept_zaaktype(self):
        catalogus = CatalogusFactory()
        zaakobjecttype = ZaakObjectTypeFactory(
            uuid=uuid4(),
            catalogus=catalogus,
            zaaktype=ZaakTypeFactory(catalogus=catalogus, concept=False),
        )

        form = ZaakObjectTypeForm(
            data={
                "uuid": str(zaakobjecttype.uuid),
                "ander_objecttype": zaakobjecttype.ander_objecttype,
                "objecttype": zaakobjecttype.objecttype,
                "relatie_omschrijving": zaakobjecttype.relatie_omschrijving,
                "zaaktype": zaakobjecttype.zaaktype.pk,
                "catalogus": zaakobjecttype.catalogus.pk,
                "datum_begin_geldigheid": date(2021, 1, 1),
                "datum_einde_geldigheid": date(2021, 2, 1),
            },
            instance=zaakobjecttype,
        )

        self.assertFalse(form.is_valid())

        error = form.errors.as_data()["__all__"][0]
        self.assertEqual(
            error.message,
            _("Objects related to non-concept objects can't be updated or created."),
        )
