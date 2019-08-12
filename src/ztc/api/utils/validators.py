from django.conf import settings
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

from rest_framework.serializers import ValidationError
from vng_api_common.constants import (
    BrondatumArchiefprocedureAfleidingswijze as Afleidingswijze
)
from vng_api_common.models import APICredential

from ztc.datamodel.constants import (
    SelectielijstKlasseProcestermijn as Procestermijn
)


def fetch_object(resource: str, url: str) -> dict:
    Client = import_string(settings.ZDS_CLIENT_CLASS)
    client = Client.from_url(url)
    client.auth = APICredential.get_auth(url)
    obj = client.retrieve(resource, url=url)
    return obj


class RelationCatalogValidator:
    code = 'relations-incorrect-catalogus'
    message = _("The {} has catalogus different from created object")

    def __init__(self, relation_field: str, catalogus_field='catalogus'):
        self.relation_field = relation_field
        self.catalogus_field = catalogus_field

    def __call__(self, attrs: dict):
        relations = attrs.get(self.relation_field)
        catalogus = attrs.get(self.catalogus_field)

        if not relations:
            return

        if not isinstance(relations, list):
            relations = [relations]

        for relation in relations:
            if relation.catalogus != catalogus:
                raise ValidationError(self.message.format(self.relation_field), code=self.code)


class ProcesTypeValidator:
    code = 'procestype-mismatch'
    message = _("{} should belong to the same procestype as {}")

    def __init__(self, relation_field: str, zaaktype_field='zaaktype'):
        self.relation_field = relation_field
        self.zaaktype_field = zaaktype_field

    def __call__(self, attrs: dict):
        selectielijstklasse_url = attrs.get(self.relation_field)
        zaaktype = attrs.get(self.zaaktype_field)

        if not selectielijstklasse_url:
            return

        selectielijstklasse = fetch_object('resultaat', selectielijstklasse_url)

        if selectielijstklasse['procesType'] != zaaktype.selectielijst_procestype:
            raise ValidationError(self.message.format(self.relation_field, self.zaaktype_field), code=self.code)


class ProcestermijnAfleidingswijzeValidator:
    code = 'invalid-afleidingswijze-for-procestermijn'
    message = _("afleidingswijze cannot be {} when selectielijstklasse.procestermijn is {}")

    def __init__(self, selectielijstklasse_field: str, archiefprocedure_field='brondatum_archiefprocedure'):
        self.selectielijstklasse_field = selectielijstklasse_field
        self.archiefprocedure_field = archiefprocedure_field

    def __call__(self, attrs: dict):
        selectielijstklasse_url = attrs.get(self.selectielijstklasse_field)
        archiefprocedure = attrs.get(self.archiefprocedure_field)

        if not selectielijstklasse_url:
            return

        selectielijstklasse = fetch_object('resultaat', selectielijstklasse_url)
        procestermijn = selectielijstklasse['procestermijn']
        afleidingswijze = archiefprocedure['afleidingswijze']

        error = False
        if procestermijn == Procestermijn.nihil and afleidingswijze != Afleidingswijze.afgehandeld:
            error = True
        elif procestermijn == Procestermijn.ingeschatte_bestaansduur_procesobject and afleidingswijze != Afleidingswijze.termijn:
            error = True

        if error:
            raise ValidationError(self.message.format(afleidingswijze, procestermijn), code=self.code)

def validate_brondatumarchiefprocedure(data: dict, mapping: dict):
    error = False
    empty = []
    required = []
    for key, value in mapping.items():
        if bool(data[key]) != value:
            error = True
            if value:
                required.append(key)
            else:
                empty.append(key)
    return error, empty, required


class BrondatumArchiefprocedureValidator:
    code = 'brondatum-archiefprocedure-invalid'
    empty_message = _('{} must be empty for afleidingswijze `{}`')
    required_message = _('{} may not be empty for afleidingswijze `{}`')

    def __init__(self, archiefprocedure_field='brondatum_archiefprocedure'):
        self.archiefprocedure_field = archiefprocedure_field

    def __call__(self, attrs: dict):
        archiefprocedure = attrs.get(self.archiefprocedure_field)
        afleidingswijze = archiefprocedure['afleidingswijze']

        mapping = {
            Afleidingswijze.afgehandeld: {
                'procestermijn': False,
                'datumkenmerk': False,
                'einddatum_bekend': False,
                'objecttype': False,
                'registratie': False
            },
            Afleidingswijze.ander_datumkenmerk: {
                'procestermijn': False,
                'datumkenmerk': True,
                'objecttype': True,
                'registratie': True
            },
            Afleidingswijze.eigenschap: {
                'procestermijn': False,
                'datumkenmerk': True,
                'objecttype': False,
                'registratie': False
            },
            Afleidingswijze.gerelateerde_zaak: {
                'procestermijn': False,
                'datumkenmerk': False,
                'objecttype': False,
                'registratie': False
            },
            Afleidingswijze.hoofdzaak: {
                'procestermijn': False,
                'datumkenmerk': False,
                'objecttype': False,
                'registratie': False
            },
            Afleidingswijze.ingangsdatum_besluit: {
                'procestermijn': False,
                'datumkenmerk': False,
                'objecttype': False,
                'registratie': False
            },
            Afleidingswijze.termijn: {
                'procestermijn': True,
                'datumkenmerk': False,
                'einddatum_bekend': False,
                'objecttype': False,
                'registratie': False
            },
            Afleidingswijze.vervaldatum_besluit: {
                'procestermijn': False,
                'datumkenmerk': False,
                'objecttype': False,
                'registratie': False
            },
            Afleidingswijze.zaakobject: {
                'procestermijn': False,
                'datumkenmerk': True,
                'objecttype': True,
                'registratie': False
            },
        }

        error, empty, required = validate_brondatumarchiefprocedure(archiefprocedure, mapping[afleidingswijze])

        if error:
            error_dict = {}
            if empty:
                error_dict.update({f'{self.archiefprocedure_field}_empty_values': [self.empty_message.format(empty, afleidingswijze)]})
            if required:
                error_dict.update({f'{self.archiefprocedure_field}_required_values': [self.required_message.format(required, afleidingswijze)]})
            raise ValidationError(error_dict, code=self.code)
