from django.utils.encoding import force_text
from django.utils.translation import ugettext

import coreapi
import coreschema
from rest_framework.filters import SearchFilter as _SearchFilter


class SearchFilter(_SearchFilter):
    def get_schema_fields(self, view):
        """
        Overriden to include the search fields by name.
        """
        search_fields = getattr(view, 'search_fields', [])

        return [
            coreapi.Field(
                name=self.search_param,
                required=False,
                location='query',
                schema=coreschema.String(
                    title=force_text(self.search_title),
                    description=ugettext(
                        'Een of meerdere zoektermen, gescheiden door een spatie. Er wordt gezocht in de velden: {}'
                    ).format(', '.join(search_fields))
                )
            )
        ]
