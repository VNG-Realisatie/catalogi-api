=================
Zaaktypecatalogus
=================

:Version: 0.7.1
:Source: https://github.com/VNG-Realisatie/zaaktypecataloguscomponent
:Keywords: zaaktypen, ztc, imztc, ztc2, ztcaas, saas, rest, api

|build-status|

Referentieimplementatie van het informatiemodel Zaaktypecatalogus (ImZTC) 2.1
welke beheerd kan worden middels een webinterface en ontsloten wordt middels
een RESTful API.

Ontwikkeld door `Maykin Media B.V. <https://www.maykinmedia.nl>`_ in opdracht
van VNG.


Introductie
===========

De GEMMA Zaaktypecatalogus 2 (ZTC2, ofwel de 2e generatie zaaktypecatalogus)
helpt gemeenten om het proces vanuit de 'vraag van een klant' (productaanvraag,
melding, aangifte, informatieverzoek e.d.) tot en met het leveren van een
passend antwoord daarop in te richten, inclusief de bijbehorende
informatievoorziening. Opslag van gegevens gebeurt conform het ImZTC (2.1).

KING heeft onderkend dat er niet één landelijke zaaktypecatalogus kan bestaan
waarin alle zaaktypen van alle overheidsorganisaties volledig uitgewerkt een
plaats hebben of krijgen. Het gevolg is dat er niet één, maar vele
zaaktypecatalogi zullen ontstaan.

De ZTC2 ondersteunt de volgende functionaliteiten:

* Webinterface voor het aanmaken, wijzigen en verwijderen van catalogi en alle
  bijbehorende zakentypen, besluittypen, etc.
* Ontsluiten van catalogi middels een RESTful API
* Uitgebreide API documentatie.

Deze component heeft ook een `testomgeving`_ waar leveranciers tegenaan kunnen
testen.

Documentatie
============

Zie ``INSTALL.rst`` voor installatie instructies, commando's en instellingen.

* `Informatiemodel Zaaktypen/Zaaktypecatalogus 2.1 (ImZTC) <http://www.gemmaonline.nl/index.php/Informatiemodel_Zaaktypen_(ImZTC)>`_
* `GEMMA Zaaktypecatalogus <https://www.gemmaonline.nl/index.php/GEMMA_Zaaktypecatalogus>`_



Verwijzingen
============

* `Ontwikkeling ZDS 2.0 standaard <https://github.com/VNG-Realisatie/gemma-zaken/>`_
* `Issues <https://github.com/VNG-Realisatie/zaaktypecataloguscomponent/issues>`_
* `Code <https://github.com/VNG-Realisatie/zaaktypecataloguscomponent>`_

.. |build-status| image:: http://jenkins.nlx.io/buildStatus/icon?job=gemma-zaaktypecatalogus-stable
    :alt: Build status
    :target: http://jenkins.nlx.io/job/gemma-zaaktypecatalogus-stable

.. |requirements| image:: https://requires.io/github/VNG-Realisatie/gemma-zaaktypecatalogus/requirements.svg?branch=master
     :target: https://requires.io/github/VNG-Realisatie/gemma-zaaktypecatalogus/requirements/?branch=master
     :alt: Requirements status

.. _testomgeving: https://ref.tst.vng.cloud/ztc/
