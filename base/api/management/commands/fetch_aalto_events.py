from django.core.management.base import BaseCommand, CommandError
import urllib2
from datetime import date, timedelta
import dateutil.parser
import re
from xml.dom.minidom import parse
from django.utils.encoding import smart_unicode
from api.geocoder import reverse_geocode
from api.models import Event
from api.utils import obj_to_json

class Command(BaseCommand):
    
    def handle(self, *args, **options):
	self.stdout.write('Getting Aalto Events stuff\n')
	
	events = self.extract_events('http://www.aalto.fi/fi/current/events/rss.xml')
	self.stdout.write('Finished, added ' + str(len(events)) + ' events\n')
	return
	
    def extract_events(self, url):
	event_urls = []
	events = []
	
	handle = urllib2.urlopen(url)
	
	dom = parse(handle)

	sanitizer_re = re.compile(r'(style|id|class)="[^"]*"')
	items = dom.getElementsByTagName('item')
	for item in items:
	    e = Event()
	    e.remote_source_name = 'AaltoEvents'
	    e.remote_url = self.getdata(item, 'link')
	    
	    if Event.objects.filter(remote_url__iexact=e.remote_url).count() > 0:
		print 'Event already exists, continuing.'
		continue
	    
	    e.title = smart_unicode(self.getdata(item, 'title'))
	    e.descr = smart_unicode(self.getdata(item, 'description'))
	    e.descr = sanitizer_re.sub('', e.descr) # Strip style, id, class attrs
	    
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
		if not point: raise Exception('No georss:point')
		
		point = point.replace(',', '.')
		point = point.split(' ')
		e.lat = float(point[0])
		e.lon = float(point[1])
	    except Exception as ex:
                #print '%s' % ex
		e.lat = 0
		e.lon = 0

	    e.org_name = smart_unicode(self.getdata(item, 'author'))
	    
	    try: 
                #print e.lat, e.lon
                if not (e.lat and e.lat != 0 and e.lon and e.lon != 0):
                    raise Exception('Missing lat or lon')
                
                res = reverse_geocode(e.lat, e.lon)
                #print res
                
                if hasattr(res, 'street_address'):
                    e.street_address = res.street_address
                else:
                    e.street_address = ''
                    
                if hasattr(res, 'city'):
                    e.city = res.city
                else:
                    e.city = ''
                    
                if hasattr(res, 'country'):
                    e.country = res.country
                else:
                    e.country = 'Finland'
	    except Exception as ex:
                #print 'Error fetching street address: %s' % ex
                e.street_address = ''
                e.city = ''
                e.country = ''
                
	    e.org_email = ''
	    e.org_phone = ''
	
            e.save()
            events.append(e)
	
	
	return events
	
    def getdata(self, src, name):
	try:
	    return src.getElementsByTagName(name)[0].firstChild.data
	except Exception:
	    return