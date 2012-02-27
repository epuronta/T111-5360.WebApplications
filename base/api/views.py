from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.db.models import Q
from api.models import Event
from api.urls import urlpatterns
from api.utils import events_to_json
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
    
	return HttpResponse(events_to_json(events), mimetype='application/json')
	
    except Exception as e:
	return HttpResponseBadRequest(e)


# Returns event (normally a single one) with given event id or 404
def single_event(request, event_id):
    event = Event.objects.filter(id=event_id)
    if not event:
	return HttpResponseNotFound()

    return HttpResponse(events_to_json(event), mimetype='application/json')