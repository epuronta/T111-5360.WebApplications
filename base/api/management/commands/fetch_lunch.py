from django.core.management.base import BaseCommand, CommandError
import urllib2
from datetime import date, timedelta
import dateutil.parser
from xml.dom.minidom import parse

from api.models.Restaurant import Restaurant
from api.models.OpeningHours import OpeningHours
from api.models.LunchList import LunchList
from api.utils import obj_to_json

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
	self.stdout.write('Handling stuff\n')
	self.process_data( self.get_data_url() )
	self.stdout.write('Finished\n')
	return
	
    def process_data(self, url):	
	handle = urllib2.urlopen(url)
	dom = parse(handle)

	campuses = dom.getElementsByTagName('campus')
	for campus in campuses:
	    
	    campusname = self.getdata(campus,'name')
	    
	    restaurants = campus.getElementsByTagName('restaurant')
	    
	    for restaurant in restaurants:
		r = Restaurant()
		r.name = self.getdata(restaurant, 'name')
		r.url = self.getdata(restaurant, 'url')
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
	
    def getdata(self, src, name):
	try:
	    return src.getElementsByTagName(name)[0].firstChild.data
	except Exception:
	    return