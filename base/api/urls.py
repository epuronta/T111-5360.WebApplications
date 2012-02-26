from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'api.views.index', name='index-view'),
    
    url(r'^events/$', 'api.views.list_events', name='list-events-view'),
    url(r'^events/(?P<event_id>\d+)/$', 'api.views.single_event', name='event-detail-view'),
    
    #url(r'^news/$', 'api.views.news', name='list-news-view'),
)
