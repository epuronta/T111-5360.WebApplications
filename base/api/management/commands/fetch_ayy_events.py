# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from api.models import Event
import urllib2
from datetime import date, timedelta
import random
from bs4 import BeautifulSoup

class Command(BaseCommand):
    args = '<num_events>'
    help = 'Generates <num_events> random events to event database'
    
    def handle(self, *args, **options):	
	
	event_listing = urllib2.urlopen('http://ayy.fi/kalenteri/')
	soup = BeautifulSoup(event_listing.read())
	
	for row in soup.find_all('tr'):
            try:
                link = row.a
                if not link: continue # No links found
                    
                detail_url = link['href']
                if detail_url == '': continue # No valid url
                
                # Get data, parse
                detail_data = urllib2.urlopen(detail_url)            
                dsoup = BeautifulSoup(detail_data.read())
                
                event = Event()
                event.remote_source_name = 'ayy'
                event.remote_url = detail_url                
                
                container = dsoup.find(id='content')
                if not container: continue;
                
                # Extract title
                event.title = container.find("h1", { "class": "main-title" }).string
                #print "Title: %s" % (title)               
                
                # Extract description
                content = container.find("div", { "class": "entry-content" })
                for c in content.find_all("script"): c.extract() # Remove scripts
                for c in content.find_all("div", { "class": "pd-rating" }): c.extract()
                event.descr = ""
                for c in content.contents: event.descr += str(c)
                #print "Descr: %s" % (contentstr[:100])
                
                metadata = content.next_sibling.next_sibling.next_sibling
                
                # Extract times
                start_time = metadata.p
                for c in start_time.find_all('b'): c.extract()
                start_time = start_time.get_text().split('\n')
                end_time = start_time[1]
                start_time = start_time[0]
                print "Start: %s, end: %s" % (start_time, end_time)
                event.start_date = None
                event.end_date = None
                
                # Extract location
                info = metadata.contents[7].get_text().split('\n')
                event.venue = info[0].split('Paikka: ')[1]
                event.street_address = info[1].split('Osoite: ')[1]
                event.city = info[2].split('Kaupunki: ')[1]
                event.country = 'Finland'
                # TODO: Resolve lat and lon from street address
                
                #print 'Loc: %s, addr: %s, city: %s' % (loc, addr, city)
                
                # Extract links
                metadata = metadata.next_sibling.next_sibling
                info = metadata.contents[3]
                links = info.find_all('a')
                homepage = links[0]['href']
                facebookev = links[1]['href']
                print 'Homepage: %s, FB: %s' % (homepage, facebookev)
                
                # Extract contact info
                info = metadata.contents[7].get_text().split('\n')
                event.org_name = info[0].split(u'Järjestäjä: ')[1]
                event.org_email = info[1].split(u'Sähköposti: ')[1]
                event.org_phone = info[2].split('Puhelin: ')[1]
                #print 'Name: %s, email: %s, phone: %s' % (org_name, org_email, org_phone)
                
                event.save()
            except Exception as e:
                print 'Error handling event: %s' % e
            print '----------------------------------------'
            #break
	
	return