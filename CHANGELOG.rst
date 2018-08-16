===========
Wijzigingen
===========

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
