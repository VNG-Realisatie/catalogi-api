"""
Defines the scopes used in the ZTC component.

We keep things extremely simple - you can either read or write. Currently
writes are not supported yet in the API.
"""
from zds_schema.scopes import Scope

SCOPE_ZAAKTYPES_READ = Scope(
    'zds.scopes.zaaktypes.lezen',
    description="""
**Laat toe om**:

* leesoperaties uit te voeren in de API. Alle resources zijn beschikbaar.
"""
)

SCOPE_ZAAKTYPES_WRITE = Scope(
    'zds.scopes.zaaktypes.schrijven',
    description="""
**Laat toe om**:

* schrijfoperaties uit te voeren in de API. Alle resources zijn beschikbaar.
"""
)
