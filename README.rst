=================
Zaaktypecatalogus
=================

:Version: 0.1.0
:Source: https://github.com/Haarlem/zaaktypecataloguscomponent
:Keywords: zaaktypen, ztc, imztc, ztc2, ztcaas, saas, rest, api

|build-status| |coverage|

Implementatie van het informatiemodel Zaaktypecatalogus (ImZTC) 2.1 welke
beheerd kan worden middels een webinterface en ontsloten wordt middels een
RESTful API.

Ontwikkeld door `Maykin Media B.V. <https://www.maykinmedia.nl>`_ in opdracht
van de Gemeente Haarlem.


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


Opmerking
=========

In afwijking van de specificatie is er geen vertaling van het ImZTC naar het
uitwisselformaat `StUF-ZTC`_ en de bijbehorende SOAP-services. Met het oog op
de toekomst is gekeken naar `RSGB Bevragingen`_ en de strategieën gebruikt in
het `Digitaal Stelsel Omgevingswet`_ (DSO).


Documentatie
============

Zie ``INSTALL.rst`` voor installatie instructies, commando's en instellingen.

* `Informatiemodel Zaaktypen/Zaaktypecatalogus 2.1 (ImZTC) <http://www.gemmaonline.nl/index.php/Informatiemodel_Zaaktypen_(ImZTC)>`_
* `GEMMA Zaaktypecatalogus <https://www.gemmaonline.nl/index.php/GEMMA_Zaaktypecatalogus>`_



Verwijzingen
============

* `Community <https://discussie.kinggemeenten.nl/discussie/gemma/ztc>`_
  (rapporteren van bugs, functionaliteit aanvragen, algemene vragen)
* `Issues <https://github.com/Haarlem/zaaktypecataloguscomponent/issues>`_
* `Code <https://github.com/Haarlem/zaaktypecataloguscomponent>`_


.. |build-status| image:: https://secure.travis-ci.org/Haarlem/zaaktypecataloguscomponent.svg?branch=master
    :alt: Build status
    :target: https://travis-ci.org/Haarlem/zaaktypecataloguscomponent

.. |coverage| image:: https://codecov.io/github/Haarlem/zaaktypecataloguscomponent/coverage.svg?branch=master
    :alt: Coverage
    :target: https://codecov.io/github/Haarlem/zaaktypecataloguscomponent?branch=master

.. _RSGB Bevragingen: https://www.gemmaonline.nl/index.php/RSGB_Bevragingen
.. _StUF-ZTC: https://www.gemmaonline.nl/index.php/Sectormodel_Zaaktypen(-catalogus):_StUF%E2%80%93ZTC
.. _Digitaal Stelsel Omgevingswet: https://aandeslagmetdeomgevingswet.nl/digitaal-stelsel/documenten/documenten/api-uri-strategie/
