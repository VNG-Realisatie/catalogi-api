=================
zaaktypecatalogus
=================

:Version: 0.1.0
:Source: https://github.com/VNG-Realisatie/gemma-zaaktypecatalogus
:Keywords: zaken, zaakgericht werken, GEMMA, RGBZ, ZTC
:PythonVersion: 3.6

|build-status|

Referentieimplementatie van de Catalogi API als zaaktypecatalogus (ZTC).

Introduction
============

Binnen het Nederlandse gemeentelandschap wordt zaakgericht werken nagestreefd.
Om dit mogelijk te maken is er gegevensuitwisseling nodig. Er is een behoefte
om zaken via een vast omlijnd proces te behandelen. Dit proces is vastgelegd in
de Catalogi API, waar andere API's naar verwijzen.

Deze referentieimplementatie toont aan dat de API specificatie voor de
zaaktypecatalogus (hierna ZTC) implementeerbaar is, en vormt een
voorbeeld voor andere implementaties indien ergens twijfel bestaat.

Deze component heeft ook een `testomgeving`_ waar leveranciers tegenaan kunnen
testen.

Dit document bevat de technische documentatie voor deze component.


Contents
========

.. toctree::
    :maxdepth: 2

    contents/installation
    contents/usage
    source/ztc
    contents/copyright
    contents/changelog


References
============

* `Issues <https://github.com/VNG-Realisatie/gemma-zaaktypecatalogus/issues>`_
* `Code <https://github.com/VNG-Realisatie/gemma-zaaktypecatalogus/>`_


.. |build-status| image:: http://jenkins.nlx.io/buildStatus/icon?job=gemma-zaaktypecatalogus-stable
    :alt: Build status
    :target: http://jenkins.nlx.io/job/gemma-zaaktypecatalogus-stable

.. |requirements| image:: https://requires.io/github/VNG-Realisatie/gemma-zaaktypecatalogus/requirements.svg?branch=master
     :target: https://requires.io/github/VNG-Realisatie/gemma-zaaktypecatalogus/requirements/?branch=master
     :alt: Requirements status

.. _testomgeving: https://catalogi-api.vng.cloud/
