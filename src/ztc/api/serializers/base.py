from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from ..utils.rest_flex_fields import FlexFieldsSerializerMixin


class ModelSerializer(FlexFieldsSerializerMixin, serializers.HyperlinkedModelSerializer):
    pass


class NestedModelSerializer(FlexFieldsSerializerMixin, NestedHyperlinkedModelSerializer):
    pass
