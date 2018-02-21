===========
Installatie
===========

De Zaakttypecatalogus is ontwikkeld in Python met behulp van het
`Django framework <https://www.djangoproject.com/>`_ en
`Django Rest Framework <http://www.django-rest-framework.org/>`_.

Voor platform specifieke installatie instructies, zie de folder
"deployment".

Zie ``CONTRIBUTING`` voor installatie instructies voor ontwikkelaars.

Voorwaarden
===========

De volgende programma's of bibliotheken dienen aanwezig te zijn:

* Python 3.4 of hoger
* Python Virtualenv en Pip
* PostgreSQL 9.1 of hoger


Instellingen
============

Alle instellingen van de Zaaktypecatalogus bevinden zich in
``src/ztc/conf``. Het bestand ``local.py`` overschrijft instellingen
uit de basis configuratie.

Er zijn geen specifieke instellingen van de Zaaktypecatalogus. Zie
`Django Rest Framework settings<http://www.django-rest-framework.org/api-guide/settings/>`_
voor alle API gerelateerde instellingen.


Commando's
==========

Commando's kunnen worden uitgevoerd middels::

    $ python src/manage.py <commando>

Naast alle standaard commando's biedt de Zaaktypecatalogus geen eigen
commando's.
