from django.core.management.base import BaseCommand, CommandError
from api.models import Event
from api.utils import obj_to_json
import urllib2
from datetime import date, timedelta
import random

class Command(BaseCommand):
    args = '<num_events>'
    help = 'Generates <num_events> random events to event database'
    
    def handle(self, *args, **options):	    
	self.stdout.write('Handled stuff\n')
	
	
	events = self.extract_events('http://ayy.fi/kalenteri/')
	for event in events:
	   self.stdout.write( obj_to_json(event))
	return
	
    def extract_events(self, url):
	event_urls = []
	events = []
	
	handle = urllib2.urlopen(url)
	print handle.read(100)
	
	event_urls.append('http://ayy.fi/blog/events/13797-2/')
	
	for url in event_urls:
	    events.append(self.extract_event(url))
	return events
	
    def extract_event(self, url):
	handle = urllib2.urlopen(url)
	print handle.read(100)
	
	e = Event()
	
	min_date = (date.today() + timedelta(days=-30)).toordinal()
	max_date = (date.today() + timedelta(days=60)).toordinal()
	
	e.start_date = random_day = date.fromordinal(random.randint(min_date, max_date))
	e.end_date = e.start_date + timedelta(0, 60 * 60) # duration 60 minutes
	
	e.title = 'Event'
	e.descr = 'Description for event'
	
	e.lat = random.randint(24000, 26000)/1000.0
	e.lon = random.randint(58000, 62000)/1000.0
	
	'''
	e.street_address = models.CharField(max_length=500)
	e.city = models.CharField(max_length=500)
	e.country = models.CharField(max_length=100)
	'''
	e.org_name = 'Sample Organizer'
	e.org_email = 'sample.organizer@org.org'
	e.org_phone = '+358501234567'
	
	e.save()
	
	return e