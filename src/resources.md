# Resources

Dit document beschrijft de (RGBZ-)objecttypen die als resources ontsloten
worden met de beschikbare attributen.


## Catalogus

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Imztc_2.1/doc/objecttype/catalogus)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url |  | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| domein | Een afkorting waarmee wordt aangegeven voor welk domein in een CATALOGUS ZAAKTYPEn zijn uitgewerkt. | string | ja | C​R​U​D |
| rsin | Het door een kamer toegekend uniek nummer voor de INGESCHREVEN NIET-NATUURLIJK PERSOON die de eigenaar is van een CATALOGUS. | string | ja | C​R​U​D |
| contactpersoonBeheerNaam | De naam van de contactpersoon die verantwoordelijk is voor het beheer van de CATALOGUS. | string | ja | C​R​U​D |
| contactpersoonBeheerTelefoonnummer | Het telefoonnummer van de contactpersoon die verantwoordelijk is voor het beheer van de CATALOGUS. | string | nee | C​R​U​D |
| contactpersoonBeheerEmailadres | Het emailadres van de contactpersoon die verantwoordelijk is voor het beheer van de CATALOGUS. | string | nee | C​R​U​D |
| zaaktypen |  | array | nee | ~~C~~​R​~~U~~​~~D~~ |
| besluittypen |  | array | nee | ~~C~~​R​~~U~~​~~D~~ |
| informatieobjecttypen |  | array | nee | ~~C~~​R​~~U~~​~~D~~ |

## BesluitType

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Imztc_2.1/doc/objecttype/besluittype)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url |  | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| catalogus | De CATALOGUS waartoe dit BESLUITTYPE behoort. | string | ja | C​R​U​D |
| zaaktypes |  | array | nee | ~~C~~​R​~~U~~​~~D~~ |
| omschrijving | Omschrijving van de aard van BESLUITen van het BESLUITTYPE. | string | ja | C​R​U​D |
| omschrijvingGeneriek | Algemeen gehanteerde omschrijving van de aard van BESLUITen van het BESLUITTYPE | string | nee | C​R​U​D |
| besluitcategorie | Typering van de aard van BESLUITen van het BESLUITTYPE. | string | nee | C​R​U​D |
| reactietermijn | Het aantal dagen, gerekend vanaf de verzend- of publicatiedatum, waarbinnen verweer tegen een besluit van het besluittype mogelijk is. Specifieer de duur als &#39;DD 00:00&#39; | string | nee | C​R​U​D |
| publicatieIndicatie | Aanduiding of BESLUITen van dit BESLUITTYPE gepubliceerd moeten worden. | boolean | nee | C​R​U​D |
| publicatietekst | De generieke tekst van de publicatie van BESLUITen van dit BESLUITTYPE | string | nee | C​R​U​D |
| publicatietermijn | Het aantal dagen, gerekend vanaf de verzend- of publicatiedatum, dat BESLUITen van dit BESLUITTYPE gepubliceerd moeten blijven. Specifieer de duur als &#39;DD 00:00&#39; | string | nee | C​R​U​D |
| toelichting | Een eventuele toelichting op dit BESLUITTYPE. | string | nee | C​R​U​D |
| informatieobjecttypes |  | array | nee | ~~C~~​R​~~U~~​~~D~~ |

## InformatieObjectType

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Imztc_2.1/doc/objecttype/informatieobjecttype)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url |  | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| omschrijving | Omschrijving van de aard van informatieobjecten van dit INFORMATIEOBJECTTYPE. | string | ja | C​R​U​D |
| catalogus | De CATALOGUS waartoe dit INFORMATIEOBJECTTYPE behoort. | string | ja | C​R​U​D |

## ZaakType

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Imztc_2.1/doc/objecttype/zaaktype)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url |  | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| identificatie | Unieke identificatie van het ZAAKTYPE binnen de CATALOGUS waarin het ZAAKTYPE voorkomt. | integer | ja | C​R​U​D |
| omschrijving | Omschrijving van de aard van ZAAKen van het ZAAKTYPE. | string | ja | C​R​U​D |
| omschrijvingGeneriek | Algemeen gehanteerde omschrijving van de aard van ZAAKen van het ZAAKTYPE | string | nee | C​R​U​D |
| doorlooptijd | De periode waarbinnen volgens wet- en regelgeving een ZAAK van het ZAAKTYPE afgerond dient te zijn, in kalenderdagen. Specifieer de duur als &#39;DD 00:00&#39; | string | ja | C​R​U​D |
| servicenorm | De periode waarbinnen verwacht wordt dat een ZAAK van het ZAAKTYPE afgerond wordt conform de geldende servicenormen van de zaakbehandelende organisatie(s). Specifieer de duur als &#39;DD 00:00&#39; | string | nee | C​R​U​D |
| catalogus | De CATALOGUS waartoe dit ZAAKTYPE behoort. | string | ja | C​R​U​D |
| statustypen |  | array | nee | ~~C~~​R​~~U~~​~~D~~ |
| eigenschappen |  | array | nee | ~~C~~​R​~~U~~​~~D~~ |
| roltypen |  | array | nee | ~~C~~​R​~~U~~​~~D~~ |
| besluittypen |  | array | nee | ~~C~~​R​~~U~~​~~D~~ |

## EigenschapSpecificatie

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Imztc_2.1/doc/objecttype/eigenschapspecificatie)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| groep | Benaming van het object of groepattribuut waarvan de EIGENSCHAP een inhoudelijk gegeven specificeert. | string | nee | C​R​U​D |
| formaat | Het soort tekens waarmee waarden van de EIGENSCHAP kunnen worden vastgelegd. | string | ja | C​R​U​D |
| lengte | Het aantal karakters (lengte) waarmee waarden van de EIGENSCHAP worden vastgelegd. | string | ja | C​R​U​D |
| kardinaliteit | Het aantal mogelijke voorkomens van waarden van deze EIGENSCHAP bij een zaak van het ZAAKTYPE. | string | ja | C​R​U​D |
| waardenverzameling | Waarden die deze EIGENSCHAP kan hebben (Gebruik een komma om waarden van elkaar te onderscheiden.) | array | nee | C​R​U​D |

## Eigenschap

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Imztc_2.1/doc/objecttype/eigenschap)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url |  | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| naam | De naam van de EIGENSCHAP | string | ja | C​R​U​D |
| definitie | De beschrijving van de betekenis van deze EIGENSCHAP | string | ja | C​R​U​D |
| toelichting | Een toelichting op deze EIGENSCHAP en het belang hiervan voor zaken van dit ZAAKTYPE. | string | nee | C​R​U​D |
| ingangsdatumObject | De datum waarop het is ontstaan. | string | ja | C​R​U​D |
| einddatumObject | De datum waarop het is opgeheven. | string | nee | C​R​U​D |
| zaaktype |  | string | nee | ~~C~~​R​~~U~~​~~D~~ |

## MogelijkeBetrokkene

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Imztc_2.1/doc/objecttype/mogelijkebetrokkene)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| betrokkene | Een betrokkene die kan gerelateerd worden aan een zaak | string | ja | C​R​U​D |
| betrokkeneType |  | string | ja | C​R​U​D |

## RolType

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Imztc_2.1/doc/objecttype/roltype)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url |  | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| zaaktype |  | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| omschrijving | Omschrijving van de aard van de ROL. | string | ja | C​R​U​D |
| omschrijvingGeneriek | Algemeen gehanteerde omschrijving van de aard van de ROL. | string | ja | C​R​U​D |
| mogelijkeBetrokkenen |  | array | ja | C​R​U​D |

## StatusType

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Imztc_2.1/doc/objecttype/statustype)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url |  | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| omschrijving | Een korte, voor de initiator van de zaak relevante, omschrijving van de aard van de STATUS van zaken van een ZAAKTYPE. | string | ja | C​R​U​D |
| omschrijvingGeneriek | Algemeen gehanteerde omschrijving van de aard van STATUSsen van het STATUSTYPE | string | nee | C​R​U​D |
| statustekst | De tekst die wordt gebruikt om de Initiator te informeren over het bereiken van een STATUS van dit STATUSTYPE bij het desbetreffende ZAAKTYPE. | string | nee | C​R​U​D |
| zaaktype |  | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| volgnummer | Een volgnummer voor statussen van het STATUSTYPE binnen een zaak. | integer | ja | C​R​U​D |
| isEindstatus | Geeft aan dat dit STATUSTYPE een eindstatus betreft. Dit gegeven is afgeleid uit alle STATUSTYPEn van dit ZAAKTYPE met het hoogste volgnummer. | boolean | nee | ~~C~~​R​~~U~~​~~D~~ |


* Create, Read, Update, Delete
