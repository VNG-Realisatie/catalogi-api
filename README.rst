============
Catalogi API
============

:Version: 1.0.0
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

==========  ==============  =============================
Versie      Release datum   API specificatie 
==========  ==============  =============================
1.0.0       2019-11-18      `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/VNG-Realisatie/gemma-zaaktypecatalogus/1.0.0/src/openapi.yaml>`_,
                            `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/VNG-Realisatie/gemma-zaaktypecatalogus/1.0.0/src/openapi.yaml>`_
==========  ==============  =============================

Zie ook: `Alle versies en wijzigingen <https://github.com/VNG-Realisatie/gemma-zaaktypecatalogus/blob/master/CHANGELOG.rst>`_

Ondersteuning
-------------

==========  ==============  ==========================  =================
Versie      Release datum   Einddatum ondersteuning     Documentatie
==========  ==============  ==========================  =================
1.x         2019-11-18      (nog niet bekend)           `Documentatie <https://vng-realisatie.github.io/gemma-zaken/standaard/catalogi/index>`_
==========  ==============  ==========================  =================

Referentie implementatie
========================

|build-status| |coverage| |docker|

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
* Bekijk de `code <https://github.com/VNG-Realisatie/gemma-zaaktypecatalogus/>`_ van de referentie implementatie.

.. _`demo omgeving`: https://catalogi-api.vng.cloud/

Licentie
========

Copyright © VNG Realisatie 2018 - 2020

Licensed under the EUPL_

.. _EUPL: LICENCE.md

.. |build-status| image:: https://travis-ci.org/VNG-Realisatie/gemma-zaaktypecatalogus.svg?branch=master
    :alt: Build status
    :target: https://travis-ci.org/VNG-Realisatie/gemma-zaaktypecatalogus

.. |requirements| image:: https://requires.io/github/VNG-Realisatie/gemma-zaaktypecatalogus/requirements.svg?branch=master
     :target: https://hub.docker.com/r/vngr/gemma-drc
     :alt: Requirements status

.. |coverage| image:: https://codecov.io/github/VNG-Realisatie/gemma-zaaktypecatalogus/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage
    :target: https://codecov.io/gh/VNG-Realisatie/gemma-zaaktypecatalogus

.. |docker| image:: https://img.shields.io/badge/docker-latest-blue.svg
    :alt: Docker image
    :target: https://hub.docker.com/r/vngr/gemma-drc/

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :alt: Code style
    :target: https://github.com/psf/black

.. |python-versions| image:: https://img.shields.io/badge/python-3.6%2B-blue.svg
    :alt: Supported Python version
    :target: https://hub.docker.com/r/vngr/gemma-drc/
