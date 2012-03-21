from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'lunch.views.index', name='lunch-index-view'),
)
