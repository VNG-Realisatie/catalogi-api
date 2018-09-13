from django.urls import path

from oauth2_provider import views as oauth2_views

oauth2_endpoint_views = [
    path('authorize/', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    path('token/', oauth2_views.TokenView.as_view(), name="token"),
    path('revoke-token/', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]

app_name = 'oauth2_provider'

urlpatterns = oauth2_endpoint_views
