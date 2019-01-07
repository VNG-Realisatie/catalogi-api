===========
Wijzigingen
===========

0.7.1 (2019-01-07)
==================

Minor text fixes

* Bumped to never zds-schema, which includes help-texts for durations
* Fixed label of some resource/relations in API spec [semantics improvement]

0.7.0 (2018-12-21)
==================

API maturity update

Breaking changes:

* Renamed StatusType.is_van to StatusType.zaaktype
* Renamed X.maaktDeelUitVan to X.catalogus

New features:

* Add download of fixture data and instructions on how to use it

Bugfixes:

* Don't compare datetimes with None

0.6.7 (2018-12-19)
==================

Increase buffer size to accomodate large headers

0.6.6 (2018-12-13)
==================

Bump Django and urllib

* urllib3<=1.22 has a CVE
* use latest patch release of Django 2.0

0.6.5 (2018-12-11)
==================

Small bugfixes

* Updated to latest zds-schema
* Added a name for the session cookie to preserve sessions on the same domain
  between components.

0.6.2 (2018-12-03)
==================

Bugfixes n.a.v. APILab voorbereiding

* Fix voor uniciteit ``RolType.omschrijvingGeneriek`` bij zaaktype
* Fix voor ontsluiten ``InformatieObjectTypes`` als catalogusonderdeel
* Meer benodigde scopes toegevoegd
* Fix toegepast om API-root zonder AUTZ te bekijken

0.6.1 (2018-11-29)
==================

Bump to zds-schema 0.17.1

* Fixes missing Location header _when_ we get create operations
* Uses generic APIVersion middleware
* Fixes server URLs in OAS

0.6.0 (2018-11-27)
==================

Stap naar volwassenere API

* Informatieobjecttypen beschikbaar gemaakt via catalogus
* Besluittypen toegevoegd aan zaaktypen
* Update naar recente zds-schema versie
* HTTP 400 errors op onbekende/invalide filter-parameters
* Docker container beter te customizen via environment variables

Breaking change
---------------

De ``Authorization`` headers is veranderd van formaat. In plaats van ``<jwt>``
is het nu ``Bearer <jwt>`` geworden.

0.5.2 (2018-11-26)
==================

Bump naar zds-schema 0.14.0 om JWT decode-problemen correct af te vangen.

0.5.1 (2018-11-22)
==================

DSO API-srategie fix

Foutberichten bevatten een ``type`` key. De waarde van deze key begint niet
langer incorrect met ``"URI: "``.

0.5.0 (2018-11-21)
==================

Autorisatie-feature release

* Autorisatie-scopes toegevoegd
* Voeg JWT client/secret management toe
* Opzet credentialstore om URLs te kunnen valideren met auth/autz
* Support toevoegd om direct OAS 3.0 te serven op
  ``http://localhost:8000/api/v1/schema/openapi.yaml?v=3``. Zonder querystring
  parameter krijg je Swagger 2.0.

0.4.0 (2018-11-19)
==================

Support voor BRC en afsluiten zaak toegevoegd

* 694b111 StatusType.volgnummer toegevoegd t.b.v. #153
* 5ab1bcd Ref. vng-Realisatie/gemma-zaken#130 -- mogelijke foutantwoorden in OAS
* febaa99 Ref. vng-Realisatie/gemma-zaken#162 -- clean up BesluitType data model
* 1063e40 Ref. vng-Realisatie/gemma-zaken#162 -- voeg besluittype toe aan API
* 7aff079 Besluittype tests
* f745d55 Correcte MIME-types voor error responses
* 0a635f4 Set up contrib.sites
* e56f090 Bump zds-schema version
* 7c2e519 Logisch attribuut "isEindstatus" toegevoegd aan StatusType
  t.b.v. US 351.
* 03a4cc7 Pin node-version
* 548d490 Publicatietekst & toelichting hebben geen lengte-limitatie

0.3.1 (2018-08-20)
==================

Kleine Quality of Life verbeteringen

* update naar ``zds-schema==0.0.26`` waarin ``RolomschrijvingGeneriek``
  verwijderd is. Dit heeft geen gevolgen voor de API spec.
* verschillende verbeteringen in de admin omgeving:
    * tonen ``uuid`` in lijstweergave
    * mogelijke betrokkenen aan ``RolType`` configureerbaar gemaakt

0.3.0 (2018-08-16)
==================

API resource toegevoegd & toolingverbeteringen

* InformatieObjectType toegevoegd t.b.v. vng-Realisatie/gemma-zaken#154
* Typo gefixed in ``bin/compile_dependencies.sh``
* Windows script toegevoegd om dependencies te comilen
  (``bin/compile_dependencies.cmd``)

0.2.2 (2018-08-15)
==================

Set wijzigingen om VNG-Realisatie/gemma-zaken#169 te implementeren:

* OAS 3.0 validator toegevoegd
* ``ZaakType`` resource uitgebreid:
    * ``servicenorm`` en ``doorlooptijd`` velden toegevoegd
    * toevoeging van mogelijke (standaard) betrokkenen bij ROLTYPEn voor een
      ZAAKTYPE
    * filter parameters toegevoegd

0.2.1 (2018-07-25)
==================

* Added missing migration

0.2.0 (2018-07-25)
==================

Aantal design decisions & reorganisatie doorgevoerd

* Docker Hub organisatie nlxio -> vngr
* Jenkins containers 100% stateless gemaakt
* Gebruik van UUID in API urls in plaats van database primary keys
* Update tooling
