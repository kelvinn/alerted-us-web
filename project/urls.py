from django.conf.urls import include, url, patterns
from django.contrib.gis import admin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page
from apps.people.views import LocationView, SettingsView, https_confirmation
from apps.people.api import LocationDetail, LocationList, UserDetail, UserList
from apps.alertdb.views import AlertDetailView
from apps.alertdb.api import AlertListAPI, AlertDetailAPI, AlertAreaAPI
from rest_framework.urlpatterns import format_suffix_patterns

admin.autodiscover()

private_apis = patterns('',
                        url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
                        url(r'^api/v1/users/$', UserList.as_view()),
                        url(r'^api/v1/users/(?P<pk>[0-9]+)/$', UserDetail.as_view()),
                        url(r'^api/v1/users/profiles/$', UserDetail.as_view()),
                        url(r'^api/v1/users/profiles/(?P<pk>[0-9]+)/$', UserDetail.as_view()),
                        url(r'^api/v1/users/locations/$', LocationList.as_view()),
                        url(r'^api/v1/users/locations/(?P<pk>[0-9]+)/$', LocationDetail.as_view()),
                        )

# A section for APIs (goes first)
# Private APIs are given a namespace in case we want to use Swagger to do API documentation
urlpatterns = [
    url(r'^', include(private_apis, namespace="private_apis")),
    url(r'^api/v1/alerts/$', AlertListAPI.as_view()),
    url(r'^api/v1/alerts/(?P<cap_slug>\w+)/$', cache_page(60*60)(AlertDetailAPI.as_view())),
    url(r'^api/v1/alerts/(?P<cap_slug>\w+)/areas/$', AlertAreaAPI.as_view()),
]

# The rest of stuff
urlpatterns = urlpatterns + [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^dashboard/$', login_required(SettingsView.as_view()), name='settings-view'),
    url(r'^dashboard/locations/$', login_required(LocationView.as_view()), name='location-view'),
    url(r'^dashboard/settings/$', login_required(SettingsView.as_view()), name='settings-view'),
    url(r'^alerts/(?P<cap_slug>\w+)/$', cache_page(60)(AlertDetailView.as_view()), name='alert-details-view'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^.well-known/acme-challenge/.*', https_confirmation, name="https_confirmation"),
]

# Flatpages
urlpatterns = urlpatterns + [
    url(r'^pages/', include('django.contrib.flatpages.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html', 'geojson'])