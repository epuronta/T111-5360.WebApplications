from django.core.management.base import BaseCommand, CommandError
import urllib2
from datetime import date, timedelta
from xml.dom.minidom import parse
import HTMLParser

from api.models.Restaurant import Restaurant
from api.models.OpeningHours import OpeningHours
from api.models.LunchList import LunchList
from api.utils import obj_to_json

'''
Fetches lunch information: Restaurants, OpeningHours, LunchLists

Uses Lounasaika.net API (http://www.lounasaika.net/api/), thanks guise!
'''
class Command(BaseCommand):    
    def get_data_url(self):
	api_base = 'http://www.lounasaika.net/api/'
	api_format = 'xml'
	api_params = {'key':'development321'}
	
	url = api_base + api_format + '?'
	for key in api_params:
	    url += key + '=' + api_params[key]
	return url
    
    def handle(self, *args, **options):
	self.stdout.write('Getting lunch lists\n')
	self.process_data( self.get_data_url() )
	self.stdout.write('Finished\n')
	return
	
    def process_data(self, url):	
	handle = urllib2.urlopen(url)
	#handle = open('api/management/commands/reply.xml', 'r')
	dom = parse(handle)
	
	htmlparser = HTMLParser.HTMLParser()

	# Delete existing opening hours
	OpeningHours.objects.all().delete()
	LunchList.objects.all().delete()
	weekdays = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
	
	# Loop through campuses
	campuses = dom.getElementsByTagName('campus')
	for campus in campuses:
	    
	    campusname = self.getdata(campus,'name')
	    
	    restaurants = campus.getElementsByTagName('restaurant')
	    
	    # Loop through campus restaurants
	    for restaurant in restaurants:
		r = Restaurant()
		r.name = self.getdata(restaurant, 'name')
		print 'Handling %s' % (r.name)
		
		r.external_url = self.getdata(restaurant, 'url')
		r.info = self.getdata(restaurant, 'info')
		if not r.info:
		    r.info = ''
		r.campus = campusname
		
		location = restaurant.getElementsByTagName('location')[0]
		r.street_address = self.getdata(location, 'address')
		
		try:
		    r.lat = float(self.getdata(location, 'lat'))
		    r.lon = float(self.getdata(location, 'lng'))
		except Exception:
		    r.lat = 0
		    r.lon = 0
		    
		r.save()
		
		# Extract opening hours for restaurant
		opening_hours = restaurant.getElementsByTagName('opening_hours')[0]
		
		for i, weekday in enumerate(weekdays):
		    #print '\tGetting opening hours for %s..' % (weekday)
		    
		    try:
			node = opening_hours.getElementsByTagName(weekday)[0]
			o = self.getdata(node, 'opening_time')
			c = self.getdata(node, 'closing_time')
			
			if not o or not c:
			    raise Exception
			
			oh = OpeningHours()
			oh.restaurant = r
			oh.weekday = i + 1
			oh.from_hour = o
			oh.to_hour = c
			
			oh.save()
			
		    except Exception:
			#print '\tBroken/missing information, continuing'
			pass
			
			
		# Extract menus for weekdays
		menu = restaurant.getElementsByTagName('menu')[0]
		
		for i, weekday in enumerate(weekdays):
		    #print '\tTrying to get menus for %s' % (weekday)
		    
		    try:
			node = menu.getElementsByTagName(weekday)[0]
			
			l = LunchList()
			l.restaurant = r
			l.weekday = i+1
			
			l.lunch = ''.join('<li>' + htmlparser.unescape(n.firstChild.nodeValue).strip() + '</li>' for n in node.childNodes)
			#print l.lunch
			
			if l.lunch == '':
			    #print '\tNo lunch, continuing'
			    continue
			
			l.save()
			
		    except Exception:
			#print '\tBroken/missing info, continuing'
			pass

    def getdata(self, src, name):
	try:
	    return src.getElementsByTagName(name)[0].firstChild.data
	except Exception:
	    return