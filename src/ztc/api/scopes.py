"""
Defines the scopes used in the ZTC component.

We keep things extremely simple - you can either read or write. Currently
writes are not supported yet in the API.
"""
from vng_api_common.scopes import Scope

SCOPE_CATALOGI_READ = Scope(
    "catalogi.lezen",
    description="""
**Laat toe om**:

* leesoperaties uit te voeren in de API. Alle resources zijn beschikbaar.
""",
)

SCOPE_DOCUMENTEN_READ = Scope(
    "documenten.lezen",
    description="""
**Laat toe om**:

* leesoperaties uit te voeren vanaf de Documenten API. Alle resources zijn beschikbaar.
""",
)

SCOPE_ZAKEN_READ = Scope(
    "zaken.lezen",
    description="""
**Laat toe om**:

* leesoperaties uit te voeren vanaf de Zaken API. Alle resources zijn beschikbaar.
""",
)

SCOPE_CATALOGI_WRITE = Scope(
    "catalogi.schrijven",
    description="""
**Laat toe om**:
* schrijfoperaties uit te voeren in de API. Alle resources zijn beschikbaar.
""",
)

SCOPE_CATALOGI_FORCED_WRITE = Scope(
    "catalogi.geforceerd-schrijven",
    description="""
**Laat toe om**:
* Gepubliceerde types geforceerd te schrijven. Alle resources zijn beschikbaar.""",
)

SCOPE_CATALOGI_FORCED_DELETE = Scope(
    "catalogi.geforceerd-verwijderen",
    description="""
**Laat toe om**:

* Gepubliceerde types geforceerd te verwijderen. Alle resources zijn beschikbaar.
""",
)
