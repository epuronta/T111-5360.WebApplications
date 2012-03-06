from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'launcher.views.index', name='launcher-index-view'),
)
