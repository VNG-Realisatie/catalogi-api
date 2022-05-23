from rest_framework import fields as drf_fields


class SourceMappingSerializerMixin(object):
    """
    Read the `Meta.source_mapping` attribute and fill the `extra_kwargs` with
    the appropriate `source` argument.
    """

    def get_extra_kwargs(self):
        extra_kwargs = super().get_extra_kwargs()

        source_mapping = getattr(self.Meta, "source_mapping", None)
        if source_mapping is not None:
            if not isinstance(source_mapping, dict):
                raise TypeError(
                    "The `source_mapping` option must be a dict. "
                    "Got %s." % type(source_mapping).__name__
                )
            for field_name, source in source_mapping.items():
                kwargs = extra_kwargs.get(field_name, {})
                kwargs["source"] = source
                extra_kwargs[field_name] = kwargs

        return extra_kwargs


def get_from_serializer_data_or_instance(field, data, serializer):
    serializer_field = serializer.fields[field]
    # TODO: this won't work with source="*" or nested references
    data_value = data.get(serializer_field.source, drf_fields.empty)
    if data_value is not drf_fields.empty:
        return data_value

    instance = serializer.instance
    if not instance:
        return None

    return serializer_field.get_attribute(instance)
