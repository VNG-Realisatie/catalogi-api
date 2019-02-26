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
| reactietermijn | Het aantal dagen, gerekend vanaf de verzend- of publicatiedatum, waarbinnen verweer tegen een besluit van het besluittype mogelijk is. | string | nee | C​R​U​D |
| publicatieIndicatie | Aanduiding of BESLUITen van dit BESLUITTYPE gepubliceerd moeten worden. | boolean | nee | C​R​U​D |
| publicatietekst | De generieke tekst van de publicatie van BESLUITen van dit BESLUITTYPE | string | nee | C​R​U​D |
| publicatietermijn | Het aantal dagen, gerekend vanaf de verzend- of publicatiedatum, dat BESLUITen van dit BESLUITTYPE gepubliceerd moeten blijven. | string | nee | C​R​U​D |
| toelichting | Een eventuele toelichting op dit BESLUITTYPE. | string | nee | C​R​U​D |
| informatieobjecttypes |  | array | nee | ~~C~~​R​~~U~~​~~D~~ |

## InformatieObjectType

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Imztc_2.1/doc/objecttype/informatieobjecttype)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url |  | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| omschrijving | Omschrijving van de aard van informatieobjecten van dit INFORMATIEOBJECTTYPE. | string | ja | C​R​U​D |
| catalogus | De CATALOGUS waartoe dit INFORMATIEOBJECTTYPE behoort. | string | ja | C​R​U​D |

## ZaakTypenRelatie

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Imztc_2.1/doc/objecttype/zaaktypenrelatie)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| zaaktype | URL referentie naar het gerelateerde zaaktype, mogelijks in een extern ZTC. | string | ja | C​R​U​D |
| aardRelatie | Omschrijving van de aard van de relatie van zaken van het ZAAKTYPE tot zaken van het andere ZAAKTYPE | string | ja | C​R​U​D |
| toelichting | Een toelichting op de aard van de relatie tussen beide ZAAKTYPEN. | string | nee | C​R​U​D |

## ZaakType

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Imztc_2.1/doc/objecttype/zaaktype)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url |  | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| identificatie | Unieke identificatie van het ZAAKTYPE binnen de CATALOGUS waarin het ZAAKTYPE voorkomt. | integer | ja | C​R​U​D |
| omschrijving | Omschrijving van de aard van ZAAKen van het ZAAKTYPE. | string | ja | C​R​U​D |
| omschrijvingGeneriek | Algemeen gehanteerde omschrijving van de aard van ZAAKen van het ZAAKTYPE | string | nee | C​R​U​D |
| vertrouwelijkheidaanduiding | Aanduiding van de mate waarin zaakdossiers van ZAAKen van dit ZAAKTYPE voor de openbaarheid bestemd zijn. Indien de zaak bij het aanmaken geen vertrouwelijkheidaanduiding krijgt, dan wordt deze waarde gezet. | string | ja | C​R​U​D |
| doel | Een omschrijving van hetgeen beoogd is te bereiken met een zaak van dit zaaktype. | string | ja | C​R​U​D |
| aanleiding | Een omschrijving van de gebeurtenis die leidt tot het starten van een ZAAK van dit ZAAKTYPE. | string | ja | C​R​U​D |
| toelichting | Een eventuele toelichting op dit zaaktype, zoals een beschrijving van het procesverloop op de hoofdlijnen. | string | nee | C​R​U​D |
| indicatieInternOfExtern | Een aanduiding waarmee onderscheid wordt gemaakt tussen ZAAKTYPEn die Intern respectievelijk Extern geïnitieerd worden. Indien van beide sprake kan zijn, dan prevaleert de externe initiatie. | string | ja | C​R​U​D |
| handelingInitiator | Werkwoord dat hoort bij de handeling die de initiator verricht bij dit zaaktype. Meestal &#39;aanvragen&#39;, &#39;indienen&#39; of &#39;melden&#39;. Zie ook het IOB model op https://www.gemmaonline.nl/index.php/Imztc_2.1/doc/attribuutsoort/zaaktype.handeling_initiator | string | ja | C​R​U​D |
| onderwerp | Het onderwerp van ZAAKen van dit ZAAKTYPE. In veel gevallen nauw gerelateerd aan de product- of dienstnaam uit de Producten- en Dienstencatalogus (PDC). Bijvoorbeeld: &#39;Evenementenvergunning&#39;, &#39;Geboorte&#39;, &#39;Klacht&#39;. Zie ook het IOB model op https://www.gemmaonline.nl/index.php/Imztc_2.1/doc/attribuutsoort/zaaktype.onderwerp | string | ja | C​R​U​D |
| handelingBehandelaar | Werkwoord dat hoort bij de handeling die de behandelaar verricht bij het afdoen van ZAAKen van dit ZAAKTYPE. Meestal &#39;behandelen&#39;, &#39;uitvoeren&#39;, &#39;vaststellen&#39; of &#39;onderhouden&#39;. Zie ook het IOB model op https://www.gemmaonline.nl/index.php/Imztc_2.1/doc/attribuutsoort/zaaktype.handeling_behandelaar | string | ja | C​R​U​D |
| doorlooptijd | De periode waarbinnen volgens wet- en regelgeving een ZAAK van het ZAAKTYPE afgerond dient te zijn, in kalenderdagen. | string | ja | C​R​U​D |
| servicenorm | De periode waarbinnen verwacht wordt dat een ZAAK van het ZAAKTYPE afgerond wordt conform de geldende servicenormen van de zaakbehandelende organisatie(s). | string | nee | C​R​U​D |
| opschortingEnAanhoudingMogelijk | Aanduiding die aangeeft of ZAAKen van dit mogelijk ZAAKTYPE kunnen worden opgeschort en/of aangehouden. | boolean | nee | C​R​U​D |
| verlengingMogelijk | Aanduiding die aangeeft of de Doorlooptijd behandeling van ZAAKen van dit ZAAKTYPE kan worden verlengd. | boolean | nee | C​R​U​D |
| verlengingstermijn | De termijn in dagen waarmee de Doorlooptijd behandeling van ZAAKen van dit ZAAKTYPE kan worden verlengd. Mag alleen een waarde bevatten als verlenging mogelijk is. | string | nee | C​R​U​D |
| trefwoorden | Een trefwoord waarmee ZAAKen van het ZAAKTYPE kunnen worden gekarakteriseerd. | array | nee | C​R​U​D |
| publicatieIndicatie | Aanduiding of (het starten van) een ZAAK dit ZAAKTYPE gepubliceerd moet worden. | boolean | nee | C​R​U​D |
| publicatietekst | De generieke tekst van de publicatie van ZAAKen van dit ZAAKTYPE. | string | nee | C​R​U​D |
| verantwoordingsrelatie | De relatie tussen ZAAKen van dit ZAAKTYPE en de beleidsmatige en/of financiële verantwoording. | array | nee | C​R​U​D |
| productenOfDiensten | Het product of de dienst die door ZAAKen van dit ZAAKTYPE wordt voortgebracht. | array | ja | C​R​U​D |
| selectielijstProcestype | Een vanuit archiveringsoptiek onderkende groep processen met dezelfde kenmerken. URL naar de referentielijsten API. | string | nee | C​R​U​D |
| catalogus | De CATALOGUS waartoe dit ZAAKTYPE behoort. | string | ja | C​R​U​D |
| statustypen |  | array | nee | ~~C~~​R​~~U~~​~~D~~ |
| resultaattypen |  | array | nee | ~~C~~​R​~~U~~​~~D~~ |
| eigenschappen |  | array | nee | ~~C~~​R​~~U~~​~~D~~ |
| informatieobjecttypen |  | array | nee | ~~C~~​R​~~U~~​~~D~~ |
| roltypen |  | array | nee | ~~C~~​R​~~U~~​~~D~~ |
| besluittypen |  | array | nee | ~~C~~​R​~~U~~​~~D~~ |
| gerelateerdeZaaktypen | De ZAAKTYPEn van zaken die relevant zijn voor zaken van dit ZAAKTYPE. | array | ja | C​R​U​D |

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

## ResultaatType

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Imztc_2.1/doc/objecttype/resultaattype)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url |  | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| zaaktype |  | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| omschrijving | Omschrijving van de aard van resultaten van het RESULTAATTYPE. | string | ja | C​R​U​D |
| resultaattypeomschrijving | Algemeen gehanteerde omschrijving van de aard van resultaten van het RESULTAATTYPE. Dit moet een URL-referentie zijn naar de referenlijst van generieke resultaattypeomschrijvingen. Im ImZTC heet dit &#39;omschrijving generiek&#39; | string | ja | C​R​U​D |
| omschrijvingGeneriek | Waarde van de omschrijving-generiek referentie (attribuut `omschrijving`) | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| selectielijstklasse | Verwijzing naar de, voor het archiefregime bij het RESULTAATTYPE relevante, categorie in de Selectielijst Archiefbescheiden van de voor het ZAAKTYPE verantwoordelijke overheidsorganisatie. Dit is een URL-referentie naar een resultaat uit de selectielijst API | string | ja | C​R​U​D |
| toelichting | Een toelichting op dit RESULTAATTYPE en het belang hiervan voor ZAAKen waarin een resultaat van dit RESULTAATTYPE wordt geselecteerd. | string | nee | C​R​U​D |
| archiefnominatie | Aanduiding die aangeeft of ZAAKen met een resultaat van dit RESULTAATTYPE blijvend moeten worden bewaard of (op termijn) moeten worden vernietigd. Indien niet expliciet opgegeven wordt dit gevuld vanuit de selectielijst.

De mapping van waarden naar weergave is als volgt:

* `blijvend_bewaren` - Het zaakdossier moet bewaard blijven en op de Archiefactiedatum overgedragen worden naar een archiefbewaarplaats.
* `vernietigen` - Het zaakdossier moet op of na de Archiefactiedatum vernietigd worden. | string | nee | C​R​U​D |


* Create, Read, Update, Delete
