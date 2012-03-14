from django.core.management.base import BaseCommand, CommandError
import urllib2
from datetime import date, timedelta
import dateutil.parser
from xml.dom.minidom import parse

from api.models_events import Event
from api.utils import obj_to_json

class Command(BaseCommand):
    
    def handle(self, *args, **options):
	self.stdout.write('Handling stuff\n')
	
	events = self.extract_events('http://www.aalto.fi/fi/current/events/rss.xml')
	for event in events:
	    #print obj_to_json(event)
	    event.save()
	self.stdout.write('Finished, added ' + str(len(events)) + ' events\n')
	return
	
    def extract_events(self, url):
	event_urls = []
	events = []
	
	handle = urllib2.urlopen(url)
	
	dom = parse(handle)

	items = dom.getElementsByTagName('item')
	for item in items:
	    e = Event()	    
	    e.remote_source_name = 'AaltoEvents'
	    e.remote_url = self.getdata(item, 'guid')
	    
	    if Event.objects.filter(remote_url__iexact=e.remote_url).count() > 0:
		print 'Event already exists, continuing.'
		continue
	    
	    e.title = self.getdata(item, 'title')
	    e.descr = self.getdata(item, 'description')
	    
	    try:
		e.start_date = dateutil.parser.parse(self.getdata(item, 'xcal:dtstart'))
	    except Exception:
		print 'Err'
	
	    try:
		e.end_date = dateutil.parser.parse(self.getdata(item, 'xcal:dtend'))
	    except Exception:
		print 'Err'
	    
	    try:
		point = self.getdata(item, 'georss:point')
		point = point.split(' ')
		e.lat = float(point[0])
		e.lon = float(point[1])
	    except Exception:
		e.lat = 0
		e.lon = 0

	    e.org_name = self.getdata(item, 'author')
	    
	    # TODO: Lookup street address based on geoloc
	    e.street_address = ''
	    e.city = ''
	    e.country = ''	    
	    e.org_email = ''
	    e.org_phone = ''
	
	    events.append(e)
	
	
	return events
	
    def getdata(self, src, name):
	try:
	    return src.getElementsByTagName(name)[0].firstChild.data
	except Exception:
	    return