from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'api.views.index', name='index-view'),
    
    url(r'^events/$', 'api.views.list_events', name='list-events-view'),
    url(r'^events/(?P<event_id>\d+)/$', 'api.views.single_event', name='event-detail-view'),
    
    #url(r'^lunch/$', 'api.views.get_lunch', name='lunch-listing-view'),
    url(r'^lunch/$', 'api.views.get_campuses', name='list-campuses-view'),
    url(r'^lunch/search/$', 'api.views.find_lunch', name='find-lunch-view'),
    url(r'^lunch/(?P<campus_name>\w+)/$' ,'api.views.get_restaurants', name='list-restaurants-view'),
    url(r'^lunch/(?P<campus_name>.+)/(?P<restaurant_name>.+)/$',\
        'api.views.single_restaurant', name='restaurant-detail-view'),
    
    
    #url(r'^news/$', 'api.views.news', name='list-news-view'),
)
