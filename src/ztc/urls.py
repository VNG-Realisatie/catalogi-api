from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, re_path
from django.views.generic.base import TemplateView

from .views import DumpDataFixtureView, DumpDataView

urlpatterns = [
    path('admin/password_reset/', auth_views.password_reset, name='admin_password_reset'),
    path('admin/password_reset/done/', auth_views.password_reset_done, name='password_reset_done'),
    path('admin/', admin.site.urls),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
            auth_views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', auth_views.password_reset_complete, name='password_reset_complete'),

    # API views
    path('api/', include('ztc.api.urls')),

    # Simply show the master template.
    path('', TemplateView.as_view(template_name='index.html')),
    path('data/', DumpDataView.as_view(), name='dumpdata'),
    path('data/fixture/', DumpDataFixtureView.as_view(), name='dumpdata-fixture'),
    path('ref/', include('zds_schema.urls')),
]

# NOTE: The staticfiles_urlpatterns also discovers static files (ie. no need to run collectstatic). Both the static
# folder and the media folder are only served via Django if DEBUG = True.
urlpatterns += staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG and 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
