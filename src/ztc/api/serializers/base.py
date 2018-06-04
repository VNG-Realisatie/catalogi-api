from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from ..utils.rest_flex_fields import FlexFieldsSerializerMixin
from ..utils.serializers import SourceMappingSerializerMixin


class ModelSerializer(FlexFieldsSerializerMixin, SourceMappingSerializerMixin, serializers.HyperlinkedModelSerializer):
    pass


class NestedModelSerializer(FlexFieldsSerializerMixin, SourceMappingSerializerMixin, NestedHyperlinkedModelSerializer):
    pass
