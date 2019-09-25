from rest_framework import serializers
from rest_framework.relations import MANY_RELATION_KWARGS


class FilterManyRelatedField(serializers.ManyRelatedField):
    def __init__(self, child_relation=None, *args, **kwargs):
        self.filter = kwargs.pop('filter')
        super().__init__(child_relation, *args, **kwargs)

    def get_attribute(self, instance):
        attribute = super().get_attribute(instance)
        if self.filter:
            return attribute.filter(**self.filter)
        return attribute


class FilterHyperlinkedRelatedField(serializers.HyperlinkedRelatedField):
    filter = None

    @classmethod
    def many_init(cls, *args, **kwargs):
        """
        add new parametr: filter = {filter_field: filter_value}
        This parameter is added only into many=True class instance
        """
        list_kwargs = {'child_relation': cls(*args, **kwargs)}
        filter_many_kwargs = MANY_RELATION_KWARGS
        for key in kwargs:
            if key in filter_many_kwargs:
                list_kwargs[key] = kwargs[key]
        list_kwargs['filter'] = kwargs.pop('filter', cls.filter)
        return FilterManyRelatedField(**list_kwargs)


class PublishedHyperlinkedRelatedField(FilterHyperlinkedRelatedField):
    filter = {'concept': False}
