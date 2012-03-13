from django.core.management.base import BaseCommand, CommandError
from api.models_events import Event
from datetime import date, timedelta
import random

class Command(BaseCommand):
    args = '<num_events>'
    help = 'Generates <num_events> random events to event database'
    
    def handle(self, *args, **options):
	if len(args) != 1:
	    self.stdout.write('Invalid argument. Provide a single integer between 1 and 10000\n')
	    return
	
	try:
	    count = int(args[0], 10)
	except ValueError:
	    count = 0
	    
	if count < 1 or count > 10000:
	    self.stdout.write('Invalid argument. Provide a single integer between 1 and 10000\n')
	    return
	
	generated = 0
	while generated < count:
	    self.generate_event(generated)
	    generated += 1
	    
	self.stdout.write('Generated ' + str(count) + ' events\n')
	return
	
    def generate_event(self, event_num):
	e = Event()
	
	min_date = (date.today() + timedelta(days=-30)).toordinal()
	max_date = (date.today() + timedelta(days=60)).toordinal()
	
	e.start_date = random_day = date.fromordinal(random.randint(min_date, max_date))
	e.end_date = e.start_date + timedelta(0, 60 * 60) # duration 60 minutes
	
	e.title = 'Event %d' % event_num
	e.descr = 'Description for event %d' % event_num
	
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
	
	return