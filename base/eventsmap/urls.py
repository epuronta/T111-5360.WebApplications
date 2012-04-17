from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'eventsmap.views.index', name='eventsmap-index-view'),
)
