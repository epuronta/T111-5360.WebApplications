# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.utils.encoding import smart_unicode
from api.models import Event
from api import geocoder
import urllib2
import datetime
import random
from bs4 import BeautifulSoup
from dateutil import parser
import re

class Command(BaseCommand):
    args = ''
    help = 'Scrapes events from AYY calendar'
    
    def handle(self, *args, **options):	
        print 'Scraping AYY event calendar'
	datere = re.compile(r'(\d+\.\d+\.\d+), (\d+)\.(\d+)')
	
	baseurl = 'http://ayy.fi/kalenteri/'
	
	url = baseurl
	fetched_main_pages = 0
	while fetched_main_pages < 6 and url:
            print 'Getting month [current+%d]: %s' % (fetched_main_pages, url)
            event_listing = urllib2.urlopen(url)
            fetched_main_pages = fetched_main_pages + 1
            soup = BeautifulSoup(event_listing.read())
            try:
                url = baseurl + soup.find(id='content').find_all('a')[1]['href']
                print 'Next url: %s' % url
            except Exception:
                print 'No next url found, this will be the last page'
                url = None
            
            for row in soup.find_all('tr'):
                try:
                    link = row.a
                    if not link: continue # No links found
                        
                    detail_url = link['href']
                    if detail_url == '': continue # No valid url
                    
                    print '\tParsing: %s' % (detail_url)
                    # Get data, parse
                    detail_data = urllib2.urlopen(detail_url)            
                    dsoup = BeautifulSoup(detail_data.read())
                    
                    event = Event()
                    event.remote_source_name = 'ayy'
                    event.remote_url = detail_url
                    
                    container = dsoup.find(id='content')
                    if not container: continue;
                    
                    # Extract title
                    try:
                        event.title = container.find("h1", { "class": "main-title" }).string
                    except Exception as e:
                        print '\tError extracting title: %s' % e
                    #print "Title: %s" % (title)               
                    
                    # Extract description
                    try:
                        content = container.find("div", { "class": "entry-content" })
                        for c in content.find_all("script"): c.extract() # Remove scripts
                        for c in content.find_all("div", { "class": "pd-rating" }): c.extract()
                        event.descr = ""
                        for c in content.contents: event.descr += str(c)
                    except Exception as e:
                        print '\tError extracting description: %s' % e
                    #print "Descr: %s" % (contentstr[:100])
                    
                    # Extract times
                    try:
                        metadata = content.next_sibling.next_sibling.next_sibling
                        start_time = metadata.p
                        for c in start_time.find_all('b'): c.extract() #Remove b tags == titles
                        start_time = start_time.get_text().split('\n') # Split remaining by line
                        end_time = start_time[1]
                        start_time = start_time[0]
                        
                        # Check if dates contain . as time separator, replace with : if so
                        s = datere.match(start_time)                        
                        if s: start_time = s.expand(r'\1 \2:\3')
                        s = datere.match(end_time)
                        if s: end_time = s.expand(r'\1 \2:\3')
                        
                        # Parse 
                        event.start_date = parser.parse(start_time, dayfirst=True)
                        event.end_date = parser.parse(end_time, dayfirst=True)
                        #print "Start: %s, end: %s" % (event.start_date, event.end_date)
                    except Exception as e:
                        print '\tError resolving date: %s' % e
                        raise e # Fatal, dates are required
                    
                    # Extract location
                    try:
                        info = metadata.contents[7].get_text().split('\n')
                        event.venue = info[0].split('Paikka: ')[1]
                        event.street_address = info[1].split('Osoite: ')[1]
                        event.city = info[2].split('Kaupunki: ')[1]
                        event.country = 'Finland'
                        
                        query = ''
                        
                        if event.street_address:
                            query += '%s, ' % self.normalize_street_address(event.street_address)
                        if event.city:
                            query += '%s, ' % event.city
                        if event.country:
                            query += '%s' % event.country
                        query = smart_unicode(query)
                        geores = geocoder.geocode(query)
                        if geores:
                            event.lat = geores['lat']
                            event.lon = geores['lon']
                        else:
                            print '\tUnable to resolve coordinates for query %s' % query
                    except Exception as e:
                        print '\tError resolving location: %s' % e
                    
                    
                    
                    #print 'Loc: %s, addr: %s, city: %s' % (loc, addr, city)
                    
                    # Extract links
                    try:
                        metadata = metadata.next_sibling.next_sibling
                        info = metadata.contents[3]
                        links = info.find_all('a')
                        homepage = links[0]['href']
                        facebookev = links[1]['href']
                    except Exception as e:
                        print '\tError resolving links: %s' % e
                    #print 'Homepage: %s, FB: %s' % (homepage, facebookev)
                    
                    # Extract contact info
                    try:
                        info = metadata.contents[7].get_text().split('\n')
                        event.org_name = info[0].split(u'Järjestäjä: ')[1]
                        event.org_email = info[1].split(u'Sähköposti: ')[1]
                        event.org_phone = info[2].split('Puhelin: ')[1]
                    except Exception as e:
                        print '\tError resolving organizer info: %s' % e
                    #print 'Name: %s, email: %s, phone: %s' % (org_name, org_email, org_phone)
                    
                    event.save()
                except Exception as e:
                    print '\tFATAL ERROR handling event, discarded'
                #print '----------------------------------------'
            #break
	
	return
	
    # Silly custom normalization for poorly formatted street addresses
    def normalize_street_address(self, address):
        if not address: return None

        address = smart_unicode(address)
        
        # Teknologier want to shorten the village street names
        address = address.replace(u'JMT', u'Jämeräntaival')
        address = address.replace(u'SMT', u'Servin Maijan tie')
        
        # Stuff after comma often indicates floor or some insignificant detail,
        # drop it
        commaloc = address.find(',')
        if commaloc > -1:
            address = address[0:commaloc]
        
        return address
            