from django.conf.urls import url, include
from rest_framework import routers

from .besluittype.views import BesluitTypeViewSet
from .catalogus.views import CatalogusViewSet

router = routers.SimpleRouter()
router.register(r'catalogussen', CatalogusViewSet)
router.register(r'besluittypen', BesluitTypeViewSet)


#API_PREFIX = r'^v(?P<version>[0-9]+(\.[0-9]+)?)'

urlpatterns = [
    url(r'^v(?P<version>\d+)/', include(router.urls)),
]
