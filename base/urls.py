from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^api/', include('api.urls')),
    url(r'^events/', include('events.urls')),
    url(r'^eventsmap/', include('eventsmap.urls')),
    url(r'^lunch/', include('lunch.urls')),
    url(r'^', include('launcher.urls')),
)

urlpatterns += staticfiles_urlpatterns()
