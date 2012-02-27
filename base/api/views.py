from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from api.models import Event
from api.urls import urlpatterns
from api.utils import events_to_json
from datetime import datetime

def index(request):
    return HttpResponse('Listing of API functionality here')
    
    
def list_events(request):
    try:
	events = Event.objects.all()
	
	if 'start' in request.GET:
	    start_time = datetime.strptime(request.GET['start'], '%Y-%m-%dT%H:%M:%S')
	    events = events.filter(start_date__gte=start_time)
	
	
	if not events:
	    return HttpResponseNotFound()
    
	return HttpResponse(events_to_json(events), mimetype='application/json')
	
    except ValueError as e:
	return HttpResponseBadRequest(e)

def single_event(request, event_id):
    event = Event.objects.filter(id=event_id)
    if not event:
	return HttpResponseNotFound()

    return HttpResponse(events_to_json(event), mimetype='application/json')