from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.db.models import Q
from api.models import Event, Restaurant, LunchList, OpeningHours
from api.urls import urlpatterns
from api.utils import objs_to_json
from datetime import datetime

# Returns a brief link list to API operations
def index(request):
    output = '<ul>'
    for op in ['events/?help', 'events/(event_id)/']:
	output += '<li><a href="%s">%s</a></li>' % (op, op)
    
    output += '</ul>'
    return HttpResponse(output)
    
# Returns JSON object containing events with given parameters as specified in helptext 
def list_events(request):
    if 'help' in request.GET:
	helptext = 'Params:<br />\
	"start_date" greater than %Y-%m-%dT%h:%M:%S,<br />\
	"end_date" less than %Y-%m-%dT%h:%M:%S,<br />\
	"q" title or descr contains,<br />\
	"offset" result set by given int,<br />\
	"limit" result set to max given int size,<br />\
	'
	return HttpResponse(helptext)
	
    try:
	events = Event.objects.order_by('start_date')
	
	if 'start_date' in request.GET:
	    start_date= datetime.strptime(request.GET['start_date'], '%Y-%m-%dT%H:%M:%S')
	    events = events.filter(start_date__gte=start_date)
	if 'end_date' in request.GET:
	    end_date = datetime.strptime(request.GET['end_date'], '%Y-%m-%dT%H:%M:%S')
	    events = events.filter(end_date__lte=end_date)
	if 'q' in request.GET:
	    events = events.filter(Q(title__contains=request.GET['q']) | Q(descr__contains=request.GET['q']))	
	if 'offset' in request.GET:
	    offset = int(request.GET['offset'])
	    events = events[offset:]
	if 'limit' in request.GET:
	    limit = int(request.GET['limit'])
	    events = events[:limit]
	
	
	if not events:
	    return HttpResponseNotFound()
    
	return HttpResponse('{' + objs_to_json(events, 'events') + '}', content_type="application/json;charset=utf-8")
	
    except Exception as e:
	return HttpResponseBadRequest(e)


# Returns event (normally a single one) with given event id or 404
def single_event(request, event_id):
    event = Event.objects.filter(id=event_id)
    if not event:
	return HttpResponseNotFound()

    output = '{'
    output += objs_to_json(event, 'events')
    output += '}'
    return HttpResponse(output, content_type='application/json;charset=utf-8')
    
    
    
def get_lunch(request):
    if 'help' in request.GET:
	helptext = 'Params:<br />\
	"restaurant" restaurant name or info<br />\
	"lunch" keyword<br />\
	"weekday" (1-7)<br />\
	"campus" name<br />\
	'
	return HttpResponse(helptext)
	
    try:
	output = '{'
	restaurants = Restaurant.objects.order_by('campus').order_by('name')
	
	if 'restaurant' in request.GET:
	    restaurants = restaurants.filter(Q(name__contains=request.GET['restaurant']) | Q(info__contains=request.GET['restaurant']))
	if 'campus' in request.GET:
            restaurants = restaurants.filter(campus__contains=request.GET['campus'])
	
	if not restaurants:
	    return HttpResponseNotFound()    
        output += objs_to_json(restaurants, 'restaurants')
        
        openinghours = OpeningHours.objects.filter(restaurant__in=restaurants).order_by('restaurant').order_by('weekday')
        lunchlists = LunchList.objects.filter(restaurant__in=restaurants).order_by('restaurant').order_by('weekday')
        
        if 'lunch' in request.GET:
          lunchlists = lunchlists.filter(lunch__contains=request.GET['lunch'])
        if 'weekday' in request.GET:
          lunchlists = lunchlists.filter(weekday__in=request.GET['weekday'])
          openinghours = openinghours.filter(weekday__in=request.GET['weekday'])
        
        if openinghours:
          output += ',' + objs_to_json(openinghours, 'openinghours')
          
        if lunchlists:
          output += ',' + objs_to_json(lunchlists, 'lunchlists')
	
	output += '}'
	return HttpResponse(output, content_type="application/json;charset=utf-8")
	
    except Exception as e:
	return HttpResponseBadRequest(e)
