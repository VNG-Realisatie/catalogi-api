## Notificaties
## Berichtkenmerken voor Catalogi API

Kanalen worden typisch per component gedefinieerd. Producers versturen berichten op bepaalde kanalen,
consumers ontvangen deze. Consumers abonneren zich via een notificatiecomponent (zoals <a href="https://notificaties-api.vng.cloud/api/v1/schema/" rel="nofollow">https://notificaties-api.vng.cloud/api/v1/schema/</a>) op berichten.

Hieronder staan de kanalen beschreven die door deze component gebruikt worden, met de kenmerken bij elk bericht.

De architectuur van de notificaties staat beschreven op <a href="https://github.com/VNG-Realisatie/notificaties-api" rel="nofollow">https://github.com/VNG-Realisatie/notificaties-api</a>.


### besluittypen

**Kanaal**
`besluittypen`

**Main resource**

`besluittype`



**Kenmerken**

* `catalogus`: URL-referentie naar de CATALOGUS waartoe dit BESLUITTYPE behoort.

**Resources en acties**


* <code>besluittype</code>: create, update, destroy


### informatieobjecttypen

**Kanaal**
`informatieobjecttypen`

**Main resource**

`informatieobjecttype`



**Kenmerken**

* `catalogus`: URL-referentie naar de CATALOGUS waartoe dit INFORMATIEOBJECTTYPE behoort.

**Resources en acties**


* <code>informatieobjecttype</code>: create, update, destroy


### zaaktypen

**Kanaal**
`zaaktypen`

**Main resource**

`zaaktype`



**Kenmerken**

* `catalogus`: URL-referentie naar de CATALOGUS waartoe dit ZAAKTYPE behoort.

**Resources en acties**


* <code>zaaktype</code>: create, update, destroy


