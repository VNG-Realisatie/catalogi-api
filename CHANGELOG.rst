===========
Wijzigingen
===========

1.2.0-rc2 (2022-06-22)
==================

* Update python requirements (e.g django upgraded to 3.2)
* Replace Gulp with Webpack
* Change ``ResultaatType.omschrijving`` max length from 20 to 30
* Change unique constraint of ``ZaakType.omschrijving`` & ``ZaakType.catalogus``
  to ``ZaakType.identificatie`` & ``ZaakType.catalogus``
* Added ``Eigenschap.catalogus``
* Added ``ZaakTypeInformatieObjectType.catalogus``
* Added ``StatusType.catalogus``

1.2.0-rc1 (2022-07-06)
==================

* Implemented history model, see the `documentation`_ for more information
* Added ``resulttaattypenOmschrijving`` and ``vastgelegdIn`` fields to ``BesluitType``
* Added ``BesluitType.resultaattypen``
* Added ``Catalogus.naam``
* Added ``Eigenschap.zaaktype``, ``Eigenschap.statustype`` and ``Eigenschap.statustype``
* Added ``InformatieObjectType.zaaktype`` and ``InformatieObjectType.besluittypen``
* Added the following fields to ``ResultaatType``:
    * ``catalogus``
    * ``besluittypen``
    * ``informatieobjecttypen``
* Added ``RolType.catalogus``
* Added ``StatusType.doorlooptijd`` and ``StatusType.eigenschappen``
* Added the following fields to ``ZaakType``:
    * ``verantwoordelijke``
    * ``zaakobjecttypen``
    * ``broncatalogus``
    * ``bronzaaktype``
* Documentation updated: Clarification of publish operation, beginGeldigheid/eindGeldigheid and beginObject/eindObject.
* Business rules `ZTC-010`_ and `ZTC-011`_ updated to allow better version management

1.1.1 (2022-06-22)
==================

Bugfix release

* Fix being able to set eindeGeldigheid=null
* [VNG-Realisatie/gemma-zaken#1976] Fixed the API schema documentation for publish actions
* Add spectral config file to fix CI build
* Fixed incorrect ETag headers and documentation in API schema

1.0.1 (2022-06-22)
==================

Bugfix release

* Fix being able to set eindeGeldigheid=null
* [VNG-Realisatie/gemma-zaken#1976] Fixed the API schema documentation for publish actions
* Add spectral config file to fix CI build

There were other reference implementation fixes between 1.0.0 and 1.0.1 that didn't
affect the API schema. For those changes, check the commit history.

1.1.0 (2021-01-08)
==================

* Added ETag headers to the several resources.
* Added HEAD-method operation to several resources.
* Fixed several field descriptions.
* Compacted common response bodies in the schema.

1.0.0 final (2019-11-18)
========================

:tada: Release the 1.0 API spec version

1.0.0-rc2 fixes (2019-11-14)
============================

Set of fixes/features in RC2

* Added unique validation on ``InformatieobjectType.catalogus`` and
  ``InformatieobjectType.omschrijving`` (constraint existed in DB before that,
  prevents crashes)
* Added unique validation on ``ZaakInformatieobjectType.zaaktype`` and
  ``ZaakInformatieobjectType.volgnummer`` (constraint existed in DB before that,
  prevents crashes)
* Added scope ``catalogi.geforceerd-verwijderen`` which allows deletion of
  published resources - intended for administrators/superusers.
* Relaxed format of ``Zaaktype.identificatie`` - now allows alpha-numeric
  strings instead of integers.

Breaking changes
----------------

* The authorization scopes are renamed - the ``zaaktypes`` prefix is replaced
  by ``catalogi``:
    - ``catalogi.lezen``
    - ``catalogi.schrijven``
    - ``catalogi.geforceerd-verwijderen`` (new)

* ``BesluitType.zaaktypes`` is renamed to ``Besluittype.zaaktypen`` to be
  more consistent.

1.0.0-rc2 fixes (2019-11-04)
============================

Set aan fixes op RC2

* Added support for (partial) updating (``PUT`` and ``PATCH`` operations)
* Added concept-validation during updates
* Fixed schema of ``GegevensGroep`` - often allowed to be ``null``
* Fixed handling of ``Zaaktype.einddatumGeldigheid`` - this is now exclusive
  instead of inclusive
* Added support for ``Zaaktype.deelzaaktypen``

Breaking changes
----------------

* On publish of ``ZaakType``, check that there are no unpublished related objects
* Changed permission errors to the correct validation errors during publishing
* Added validation that requires related objects to belong to the same catalogus
* Filtering on bad/unexpected URLs now returns an empty result list instead
  of validation errors.


1.0.0-rc2 (2019-09-19)
======================

Second release candidate.

* Documented the validation rules for ``Zaaktype`` create
* Documented the possible options for ``ResultaatType.afleidingswijze``
* Documented the possible options for ``Objecttype``
* Fixed dumpdata fixture view (thanks Bart Jeukendrup)
* Added notifications channels for ``Zaaktype``, ``Besluittype`` and ``Infomratieobjecttype``
* Updated dependencies to latest stable/secure versions
* Fixed issue with incorrect serialization if ``Resultaattype.archiefactietermijn``
  derived from ``selectielijstklasse``
* Added validation of query parameters to all endpoints taking filter parameters

Breaking changes
----------------

* Normalized enums to be lowercased, alpha-numeric with underscores only:
    - ``EigenschapSpecificatie.formaat``
* Added explicit UniqueTogetherValidator for ``Besluittype.catalogus`` and
  ``Besluittype.omschrijving``
* Added date overlap validation in ZTC while writing ``Zaaktype`` objects
* Added resource validation for ``Zaaktype.selectielijstProcestype``
* Added resource validation for ``Resultaattype.selectielijstklasse``
* Added procestype match validation on ``Resultaattype.selectielijstklasse`` and
  ``Resultaattype.zaaktype``
* Added initial validation for ``Resultaattype.brondatumArchiefprocedure.afleidingwijze``
  based on ``selectielijstklasse.procestermijn``
* Added validation to ``Resultaattype.brondatumArchiefprocedure``

1.0.0-rc1 (2019-07-18)
======================

Release candidate tag

* Bumped to vng-api-common 1.0.0
* Bumped version numbers to 1.0.0-rc

Breaking changes
----------------

* ``RolType.mogelijkeBetrokkenen`` verwijderd

0.16.1 (2019-07-17)
===================

Consistency & bugfix release

Includes the 0.16.0 changelog.

* Updated to latest vng-api-common
* Updated documentation
* Added ``StatusType.informeren``
* Fixed resource validation for ``ResultaatType.resultaattypeomschrijving``

Breaking changes
----------------

* Renamed constants *snake_case* format
* Replaced ``JaNee`` enum with ``BooleanField``
* Lowercased relation names (``statusType`` etc. to ``statustype``)

0.15.0 (2019-07-15)
===================

Maturity improvement

* Added create/destroy actions to resources, making the ZTC writable
* Removed ``datumBeginGeldigheid`` and ``datumEindeGeldigheid`` from models
  directly linked to ``Zaaktype`` - this is derived from ``Zaaktype`` instead
* Added ``concept`` (=draft) fields to resources. Resources may be modified
  as long as they're in 'concept' status. Once concept status is set to
  ``false``, no modifications are allowed, not on related objects either.
* Added filters for concept/published/all status
* Added filters for relations (catalogus, zaaktype...)
* Added pagination to the collections
* Update to Django LTS version (2.2)
* Set up CI/CD for ``develop`` branch as well
* Improved admin interface w/r to ``ArrayField`` presentation/UI
* Added management command to migrate to new domains

0.14.2 (2019-07-02)
===================

Fixed URL reversing in the admin

0.14.1 (2019-07-01)
===================

Fixed bug in docker start script preventing fixtures from being loaded.

0.14.0 (2019-06-18)
===================

Zaaktype-versioning & small features release

* Added ``Zaaktype.beginGeldigheid`` and ``Zaaktype.eindGeldigheid``, which
  determine when a ``Zaaktype`` is 'active'
* Dropped unique constraint on ``(catalogus, identificatie)`` and added a check
  on ``beginGeldigheid`` - ``eindGeldigheid`` ranges. They may not overlap for
  a given ``(catalogus, identificatie)`` combination. This effectively allows
  you to create new versions of ``Zaaktype``.
* Bumped dependencies to latest security releases
* Translated API specs
* Added fixture loading to container startup script

0.13.0 (2019-05-31)
===================

Quality of life update

* Enabled notifications application so that ZTC can subscribe to
  ``autorisaties`` channel
* Fixed bunch of translations
* Added ``Zaaktype.beginGeldigheid`` and ``Zaaktype.eindGeldigheid`` in the
  admin. These are now taken into account when creating ``Zaaktype`` objects,
  so you can have multiple zaaktypen in the same catalogus as long as the
  date ranges do not overlap.
* Pinned the dev dependencies to prevent ``isort`` versions from creating
  chaos. We don't like chaos, or at least not that kind.
* Added a page to check the (authorization) configuration for the provider.
  This should make it easier to pinpoint mis-configuration.

0.12.0 (2019-05-20)
===================

Migrated to new auth machinery

* this is a breaking change - old JWTs with scopes included will continue to
  work for a short time if the authorization is defined in the AC
* You need to configure the AC to use
* Renamed the scope labels - the ``zds.scopes`` prefix was dropped
* Bumped various dependencies so that security fixes are applied

0.11.1 (2019-05-02)
===================

Bugfix & convenience release

* Fixed serialization of ``relativedelta`` fields
* Fixed editing/representation of ``relativedelta`` fields
* Made ``zaaktype`` URL-path copy-pasteable in the admin

0.11.0 (2019-04-16)
===================

API-lab release

* Improved homepage layout, using vng-api-common boilerplate
* Bumped to latest bugfix release of gemma-zds-client
* ``Resultaattype.selectielijstklasse`` now has resource validation with better
  error feedback in the admin
* Some UUIDs are now exposed in the admin interface

0.10.3 (2019-04-09)
===================

Fixed the admin interface for Resultaattype

0.10.2 (2019-04-02)
===================

Fixed str representation of InformatieObjectType

0.10.1 (2019-04-02)
===================

Bugfixes in the admin interface

* Fixed crash when ``RolType.zaaktype`` was an invalid choice
* Fixed crash when ``StatusType.zaaktype`` was an invalid choice
* Fixed crash when no ``BooleanRadioField`` choice was selected
* Fixed crash when no ``scopes`` key was present in the JWT claims

0.10.0 (2019-03-28)
===================

Quality of life update

* replaced duration fields ``archiefactietermijn``, ``brondatum_archiefprocedure_procestermijn``
  to be more precise (years, months...) instead of being limited to days
* added URL to license (gemma-zaken#820)
* added ``InformatieObjectType.vertrouwelijkheidaanduiding``, which is a *required*
  field
* replaced zds-schema with vng-api-common. Make sure to run
  ``python manage.py migrate_from_zds_schema`` to migrate the database contents

0.9.1 (2019-03-04)
==================

Security release

* Bumped Django to 2.0.13

0.9.0 (2019-02-27)
==================

Archiving feature release

* added read-only ``Resultaattype`` resource to API
* added ``Zaaktype.resultaattypen`` list of URLs
* added ``brondatumArchiefProcedure`` as part of ``Resultaattype`` resource
  * contains strategy on how to determine ``brondatum``
  * validated against 'Gemeentelijke Selectielijst 2017' where possible
* ``Resultaattype`` is linked to GS 2017 + validations implemented
* added ``format: duration`` to duration-attributes

0.8.2 (2019-02-07)
==================

Bump dependencies to get latest bugfixes

* Bump to zds-schema 0.20.6
* Bump to Django 2.0.10

0.8.1 (2019-01-30)
==================

Fixed bug in URL-resolution Zaaktype.informatieobjecttypen

0.8.0 (2019-01-30)
==================

API-maturity feature release

* Expose more fields/attributes of ``ZaakType`` resource:
    * ``ZaakType.vertrouwelijkheidaanduiding``
    * ``ZaakType.doel``
    * ``ZaakType.aanleiding``
    * ``ZaakType.toelichting``
    * ``ZaakType.indicatieInternOfExtern``
    * ``ZaakType.handelingInitiator``
    * ``ZaakType.onderwerp``
    * ``ZaakType.handelingBehandelaar``
    * ``ZaakType.opschorting``
    * ``ZaakType.verlengingMogelijk``
    * ``ZaakType.publicatieIndicatie``
    * ``ZaakType.verlengingstermijn`` - ISO-8601 duration
    * ``ZaakType.trefwoorden`` - list of keywords
    * ``ZaakType.publicatietekst``
    * ``ZaakType.verantwoordingsrelatie``
    * ``ZaakType.referentieproces``
    * ``ZaakType.productenOfDiensten`` - list of external URLs
    * ``ZaakType.selectielijstProcestype`` - URL reference to
      referentie/selectielijsten API
    * ``ZaakType.informatieobjecttypen`` - list of URLs to
      ``InformatieobjectType`` resources
    * ``ZaakType.gerelateerdeZaaktypen`` - list of objects containing relation
      information

* Provide the ``ZaakTypeInformatieObjectType`` resource in the root of the API.
  This allows clients to look up the relation information between ``ZaakType``
  and ``InformatieobjectType``. Possibly we might *enforce* the usage of filter
  parameters to anticipate performance challenges, or introduce pagination.

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

.. _documentation: https://vng-realisatie.github.io/gemma-zaken/standaard/catalogi/#historiemodel-catalogi-api
.. _ZTC-010: https://vng-realisatie.github.io/gemma-zaken/standaard/catalogi/#ztc-010
.. _ZTC-011: https://vng-realisatie.github.io/gemma-zaken/standaard/catalogi/#ztc-011

