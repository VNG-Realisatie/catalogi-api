# from rest_framework.relations import HyperlinkedRelatedField
#
#
# class HyperlinkedRelatedField2(HyperlinkedRelatedField):
#
#     def __init__(self, lookup_kwargs, **kwargs):
#         self.lookup_kwargs = lookup_kwargs
#         super(HyperlinkedRelatedField2, self).__init__(**kwargs)
#
#     def get_object(self, view_name, view_args, view_kwargs):
#         """
#         Return the object corresponding to a matched URL.
#
#         Takes the matched URL conf arguments, and should return an
#         object instance, or raise an `ObjectDoesNotExist` exception.
#         """
#         # assert False, view_kwargs
#         print('hoooooooooooooooi')
#         lookup_value = view_kwargs[self.lookup_url_kwarg]
#         lookup_kwargs = {self.lookup_field: lookup_value}
#         print()
#         print()
#         print()
#         print()
#         print()
#         print(lookup_kwargs)
#         return self.get_queryset().get(**lookup_kwargs)
#
#     def get_url(self, obj, view_name, request, format):
#         """
#         Given an object, return the URL that hyperlinks to the object.
#
#         May raise a `NoReverseMatch` if the `view_name` and `lookup_field`
#         attributes are not configured to correctly match the URL conf.
#         """
#         # Unsaved objects will not yet have a valid URL.
#         if hasattr(obj, 'pk') and obj.pk in (None, ''):
#             return None
#
#         return self.reverse(view_name, kwargs=self.lookup_kwargs, request=request, format=format)
#
#
# from rest_framework.reverse import reverse
# from ztc.datamodel.models import ZaakType
#
#
# class HyperlinkedRelatedField3(HyperlinkedRelatedField):
#     # view_name = 'api:zaaktype-detail'
#     queryset = ZaakType.objects.all()
#
#     def get_url(self, obj, view_name, request, format):
#         """
#         """
#
#         # url_kwargs = {
#         #     'pk': obj.is_relevant_voor.pk,
#         #     'catalogus_pk': obj.is_relevant_voor.maakt_deel_uit_van.pk
#         # }
#
#         print()
#         print()
#         print()
#         print(type(obj))
#         print(obj.__dict__)
#         print()
#         print()
#         print()
#         print(view_name)
#         print()
#         print()
#         print()
#         print()
#         print()
#         print(format)
#         print()
#         print()
#         print()
#         print()
#         print()
#
#
#         url_kwargs = {
#             'catalogus_pk': 'is_relevant_voor__maakt_deel_uit_van__pk',
#             'pk': 'is_relevant_voor__pk'
#
#         }
#
#         # url_kwargs = {
#         #     'organization_slug': obj.organization.slug,
#         #     'customer_pk': obj.pk
#         # }
#         return reverse(view_name, kwargs=url_kwargs, request=request, format=format)
#
#     # def get_object(self, view_name, view_args, view_kwargs):
#     #     print(view_kwargs)
#     #     print(view_kwargs)
#     #     print(view_kwargs)
#     #     print(view_kwargs)
#     #     print(view_kwargs)
#     #     print(view_kwargs)
#     #
#     #     lookup_kwargs = {
#     #        'organization__slug': view_kwargs['organization_slug'],
#     #        'pk': view_kwargs['customer_pk']
#     #     }
#     #     return self.get_queryset().get(**lookup_kwargs)
#
