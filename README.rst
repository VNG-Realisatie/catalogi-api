============
Catalogi API
============

:Version: 1.0.1
:Source: https://github.com/VNG-Realisatie/zaaktypecataloguscomponent
:Keywords: zaaktypen, ztc, imztc, ztc2, ztcaas, saas, rest, api

Introductie
===========

De Catalogi API is gebaseerd op de GEMMA Zaaktypencatalogus (ZTC2, ofwel de
2e generatie zaaktypecatalogus) en helpt gemeenten om het proces vanuit de
'vraag van een klant' (productaanvraag, melding, aangifte, informatieverzoek
e.d.) tot en met het leveren van een passend antwoord daarop in te richten,
inclusief de bijbehorende informatievoorziening.

API specificaties
=================
|lint-oas| |generate-sdks| |generate-postman-collection|

==========  ==============  ====================================================================================================================================================================================================  =======================================================================================================================  =================================================================================================================================
Versie      Release datum   API specificatie                                                                                                                                                                                      Autorisaties                                                                                                             Notificaties
==========  ==============  ====================================================================================================================================================================================================  =======================================================================================================================  =================================================================================================================================
1.0.1       2022-06-22      `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/VNG-Realisatie/catalogi-api/1.0.1/src/openapi.yaml>`_,                                                                 `Scopes <https://github.com/VNG-Realisatie/catalogi-api/blob/1.0.1/src/autorisaties.md>`_                                `Berichtkenmerken <https://github.com/VNG-Realisatie/catalogi-api/blob/1.0.1/src/notificaties.md>`_
                            `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/VNG-Realisatie/catalogi-api/1.0.1/src/openapi.yaml>`_
1.0.0       2019-11-18      `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/VNG-Realisatie/catalogi-api/1.0.0/src/openapi.yaml>`_,                                                                 `Scopes <https://github.com/VNG-Realisatie/catalogi-api/blob/1.0.0/src/autorisaties.md>`_                                `Berichtkenmerken <https://github.com/VNG-Realisatie/catalogi-api/blob/1.0.0/src/notificaties.md>`_
                            `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/VNG-Realisatie/catalogi-api/1.0.0/src/openapi.yaml>`_
==========  ==============  ====================================================================================================================================================================================================  =======================================================================================================================  =================================================================================================================================

Zie ook: `Alle versies en wijzigingen <https://github.com/VNG-Realisatie/catalogi-api/blob/master/CHANGELOG.rst>`_

Ondersteuning
-------------

==========  ==============  ==========================  =================
Versie      Release datum   Einddatum ondersteuning     Documentatie
==========  ==============  ==========================  =================
1.x         2019-11-18      (nog niet bekend)           `Documentatie <https://vng-realisatie.github.io/gemma-zaken/standaard/catalogi/index>`_
==========  ==============  ==========================  =================

Referentie implementatie
========================

|build-status| |coverage| |docker| |black| |python-versions|

Referentieimplementatie van de Catalogi API. Ook wel
Zaaktypencatalogus (ZTC) genoemd.

Ontwikkeld door `Maykin Media B.V. <https://www.maykinmedia.nl>`_ in opdracht
van VNG Realisatie.

Deze referentieimplementatie toont aan dat de API specificatie voor de
Catalogi API implementeerbaar is, en vormt een voorbeeld voor andere
implementaties indien ergens twijfel bestaat.

Deze component heeft ook een `demo omgeving`_ waar leveranciers tegenaan kunnen
testen.

Links
=====

* Deze API is onderdeel van de `VNG standaard "API's voor Zaakgericht werken" <https://github.com/VNG-Realisatie/gemma-zaken>`_.
* Lees de `functionele specificatie <https://vng-realisatie.github.io/gemma-zaken/standaard/catalogi/index>`_ bij de API specificatie.
* Bekijk de `demo omgeving`_ met de laatst gepubliceerde versie.
* Bekijk de `test omgeving <https://catalogi-api.test.vng.cloud/>`_ met de laatste ontwikkel versie.
* Rapporteer `issues <https://github.com/VNG-Realisatie/gemma-zaken/issues>`_ bij vragen, fouten of wensen.
* Bekijk de `code <https://github.com/VNG-Realisatie/catalogi-api/>`_ van de referentie implementatie.

.. _`demo omgeving`: https://catalogi-api.vng.cloud/

Licentie
========

Copyright © VNG Realisatie 2018 - 2020

Licensed under the EUPL_

.. _EUPL: LICENCE.md

.. |build-status| image:: https://github.com/VNG-Realisatie/catalogi-api/workflows/ci-build/badge.svg
    :alt: Build status
    :target: https://github.com/VNG-Realisatie/catalogi-api/actions?query=workflow%3Aci-build

.. |requirements| image:: https://requires.io/github/VNG-Realisatie/catalogi-api/requirements.svg?branch=master
     :alt: Requirements status

.. |coverage| image:: https://codecov.io/github/VNG-Realisatie/catalogi-api/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage
    :target: https://codecov.io/gh/VNG-Realisatie/catalogi-api

.. |docker| image:: https://img.shields.io/badge/docker-latest-blue.svg
    :alt: Docker image
    :target: https://hub.docker.com/r/vngr/gemma-ztc/

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :alt: Code style
    :target: https://github.com/psf/black

.. |python-versions| image:: https://img.shields.io/badge/python-3.6%2B-blue.svg
    :alt: Supported Python version

.. |lint-oas| image:: https://github.com/VNG-Realisatie/catalogi-api/workflows/lint-oas/badge.svg
    :alt: Lint OAS
    :target: https://github.com/VNG-Realisatie/catalogi-api/actions?query=workflow%3Alint-oas

.. |generate-sdks| image:: https://github.com/VNG-Realisatie/catalogi-api/workflows/generate-sdks/badge.svg
    :alt: Generate SDKs
    :target: https://github.com/VNG-Realisatie/catalogi-api/actions?query=workflow%3Agenerate-sdks

.. |generate-postman-collection| image:: https://github.com/VNG-Realisatie/catalogi-api/workflows/generate-postman-collection/badge.svg
    :alt: Generate Postman collection
    :target: https://github.com/VNG-Realisatie/catalogi-api/actions?query=workflow%3Agenerate-postman-collection

.. _testomgeving: https://ref.tst.vng.cloud/ztc/
