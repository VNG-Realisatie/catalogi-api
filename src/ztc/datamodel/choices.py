from django.utils.translation import ugettext_lazy as _

from djchoices import ChoiceItem, DjangoChoices

# Waardenverzameling nemen we letterlijk over. Dit betekend dat we onder
# andere de volgende waarden verwachten (en kleine afwijking hiervan zal dus
# niet valideren):
#
# Eigenschap.formaat: 'datum/tijd (jjjjmmdduummss)' dus inclusief het deel tussen haakjes
# ZaakType.vertrouwelijkheidsaanduiding: 'ZEER GEHEIM' (dus geheel in hoofdletters met spatie)
# ResultaatType.archiefnominatie: 'Blijvend bewaren' (alleen eerste is hoofdletter en een spatie)
# ResultaatType.brondatum_archiefprocedure: 'afgehandeld' dus geheel met kleine letters


class FormaatChoices(DjangoChoices):
    tekst = ChoiceItem('tekst', _('Tekst'))
    getal = ChoiceItem('getal', _('Getal'))
    datum = ChoiceItem('datum (jjjjmmdd)', _('Datum'))
    datum_tijd = ChoiceItem('datum/tijd (jjjjmmdduummss)', _('Datum/tijd'))


class ArchiefProcedure(DjangoChoices):
    afgehandeld = ChoiceItem('afgehandeld', _('Afgehandeld'))
    ingangsdatum_besluit = ChoiceItem('ingangsdatum_besluit', _('Ingangsdatum besluit'))
    vervaldatum_besluit = ChoiceItem('vervaldatum_besluit', _('Vervaldatum besluit'))
    eigenschap = ChoiceItem('eigenschap', _('Eigenschap'))
    ander_datumkenmerk = ChoiceItem('ander_datumkenmerk', _('Ander datumkenmerk'))


class ObjectTypen(DjangoChoices):
    """
    Objecttypen uit het RSGB of het RGBZ
    Zoals gedefinieerd in de waardenverzameling voor het veld 'objecttype' op het model ZaakObjectType
    """
    ander_natuurlijk_persoon = ChoiceItem('ANDER NATUURLIJK PERSOON', _('ander natuurlijk persoon'))
    ander_buitenlands_niet_natuurlijk_persoon = ChoiceItem('ANDER BUITENLANDS NIET-NATUURLIJK PERSOON', _('ander buitenlands niet natuurlijk persoon'))
    appartementsrecht = ChoiceItem('APPARTEMENTSRECHT', _('appartementsrecht'))
    besluit = ChoiceItem('BESLUIT', _('besluit'))
    buurt = ChoiceItem('BUURT', _('buurt'))
    enkelvoudig_informatieobject = ChoiceItem('ENKELVOUDIG INFORMATIEOBJECT', _('enkelvoudig informatieobject'))
    gemeente = ChoiceItem('GEMEENTE', _('gemeente'))
    gemeentelijkeopenbare_ruimte = ChoiceItem('GEMEENTELIJKEOPENBARE RUIMTE', _('gemeentelijkeopenbare ruimte'))
    huishouden = ChoiceItem('HUISHOUDEN', _('huishouden'))
    ingeschreven_niet_natuurlijk_persoon = ChoiceItem('INGESCHREVEN NIET-NATUURLIJK PERSOON', _('ingeschreven niet natuurlijk persoon'))
    ingezetene = ChoiceItem('INGEZETENE', _('ingezetene'))
    inrichtingselement = ChoiceItem('INRICHTINGSELEMENT', _('inrichtingselement'))
    kadastraal_perceel = ChoiceItem('KADASTRAAL PERCEEL', _('kadastraal perceel'))
    kunstwerkdeel = ChoiceItem('KUNSTWERKDEEL', _('kunstwerkdeel'))
    ligplaats = ChoiceItem('LIGPLAATS', _('ligplaats'))
    maatschappelijke_activiteit = ChoiceItem('MAATSCHAPPELIJKE ACTIVITEIT', _('maatschappelijke activiteit'))
    medewerker = ChoiceItem('MEDEWERKER', _('medewerker'))
    niet_ingezetene = ChoiceItem('NIET-INGEZETENE', _('niet ingezetene'))
    nummeraanduiding = ChoiceItem('NUMMERAANDUIDING', _('nummeraanduiding'))
    openbare_ruimte = ChoiceItem('OPENBARE RUIMTE', _('openbare ruimte'))
    organisatorische_eenheid = ChoiceItem('ORGANISATORISCHE EENHEID', _('organisatorische eenheid'))
    overige_adresseerbaar_objectaanduiding = ChoiceItem('OVERIGE ADRESSEERBAAR OBJECTAANDUIDING', _('overige adresseerbaar objectaanduiding'))
    overig_gebouwd_object = ChoiceItem('OVERIG GEBOUWD OBJECT', _('overig gebouwd object'))
    overig_terrein = ChoiceItem('OVERIG TERREIN', _('overig terrein'))
    pand = ChoiceItem('PAND', _('pand'))
    samengesteld_informatieobject = ChoiceItem('SAMENGESTELD INFORMATIEOBJECT', _('samengesteld informatieobject'))
    spoorbaandeel = ChoiceItem('SPOORBAANDEEL', _('spoorbaandeel'))
    standplaats = ChoiceItem('STANDPLAATS', _('standplaats'))
    status = ChoiceItem('STATUS', _('status'))
    terreindeel = ChoiceItem('TERREINDEEL', _('terreindeel'))
    verblijfsobject = ChoiceItem('VERBLIJFSOBJECT', _('verblijfsobject'))
    vestiging = ChoiceItem('VESTIGING', _('vestiging'))
    waterdeel = ChoiceItem('WATERDEEL', _('waterdeel'))
    wegdeel = ChoiceItem('WEGDEEL', _('wegdeel'))
    wijk = ChoiceItem('WIJK', _('wijk'))
    woonplaats = ChoiceItem('WOONPLAATS', _('woonplaats'))
    woz_deelobject = ChoiceItem('WOZ-DEELOBJECT', _('woz deelobject'))
    woz_object = ChoiceItem('WOZ-OBJECT', _('woz object'))
    woz_waarde = ChoiceItem('WOZ-WAARDE', _('woz waarde'))
    zakelijk_recht = ChoiceItem('ZAKELIJK RECHT', _('zakelijk recht'))


class InternExtern(DjangoChoices):
    intern = ChoiceItem('intern', _('Intern'))
    extern = ChoiceItem('extern', _('Extern'))


class RichtingChoices(DjangoChoices):
    inkomend = ChoiceItem('inkomend', _('Inkomend'))
    intern = ChoiceItem('intern', _('Intern'))
    uitgaand = ChoiceItem('uitgaand', _('Uitgaand'))


class ArchiefNominatieChoices(DjangoChoices):
    blijvend_bewaren = ChoiceItem('blijvend_bewaren', _('Blijvend bewaren'))
    vernietigen = ChoiceItem('vernietigen', _('Vernietigen'))


class AardRelatieChoices(DjangoChoices):
    vervolg = ChoiceItem('vervolg', _('Vervolg'))  # een zaak van het ZAAKTYPE is een te plannen vervolg op een zaak van het andere ZAAKTYPE
    bijdrage = ChoiceItem('bijdrage', _('Bijdrage'))  # een zaak van het ZAAKTYPE levert een bijdrage aan het bereiken van de uitkomst van een zaak van het andere ZAAKTYPE
    onderwerp = ChoiceItem('onderwerp', _('Onderwerp'))  # een zaak van het ZAAKTYPE heeft betrekking op een zaak van het andere ZAAKTYPE of een zaak van het andere ZAAKTYPE is relevant voor of is onderwerp van een zaak van het ZAAKTYPE
