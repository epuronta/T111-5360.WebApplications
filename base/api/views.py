from django.http import HttpResponse, HttpResponseNotFound
from api.models import Event
from api.urls import urlpatterns
from api.utils import events_to_json

def index(request):
    return HttpResponse('Listing of API functionality here')
    
    
def list_events(request):
    events = Event.objects.all()
    if not events:
	return HttpResponseNotFound()
    
    return HttpResponse(events_to_json(events), mimetype='application/json')

def single_event(request, event_id):
    event = Event.objects.filter(id=event_id)
    if not event:
	return HttpResponseNotFound()

    return HttpResponse(events_to_json(event), mimetype='application/json')