import urllib, urllib2
from xml.dom.minidom import parse

def geocode(query):
    # Construct url
    params = urllib.urlencode({ 'format':'xml', 'q':query.encode('utf-8') })    
    url = u'http://nominatim.openstreetmap.org/search?%s' % params
    handle = urllib2.urlopen(url)
    
    dom = parse(handle)

    # Get the result root, return if not found
    # Always use the first item, there shouldn't be more
    items = dom.getElementsByTagName('searchresults')
    if not items or len(items) < 1: return None
        
    item = items[0]
    
    # Get the first place element, we don't want to compare secondary results
    places = item.getElementsByTagName('place')
    if not places or len(places) < 1: return None
    place = places[0]
    
    lat = place.getAttribute('lat')
    lon = place.getAttribute('lon')
    
    return { 'lat': lat, 'lon': lon }
    
def reverse_geocode(lat, lon):
    
    if not lat or not lon:
        return None
        
    params = urllib.urlencode({'format': 'xml', 'lat': lat, 'lon': lon})
    url = 'http://nominatim.openstreetmap.org/reverse?%s' % params
    handle = urllib2.urlopen(url)
    
    dom = parse(handle)
    # Get the result root, return if not found
    # Always use the first item, there shouldn't be more
    items = dom.getElementsByTagName('reversegeocode')
    if not items or len(items) < 1: return None
        
    item = items[0]
    
    # Get the first place element, we don't want to compare secondary results
    parts = item.getElementsByTagName('addressparts')
    if not parts or len(parts) < 1: return None
    part = parts[0]
    
    result = { 'street_address': None, 'city': None, 'country': None}
    
    try:
        result['street_address'] = part.getElementsByTagName('road')[0].firstChild.data
        if result['street_address']:
            result['street_address'] += ' %s' % part.getElementsByTagName('house_number')[0].firstChild.data
    except Exception as ex:
        #print 'Error extracting street address: %s'  % ex
        pass
    
    try:
        result['city'] = part.getElementsByTagName('city')[0].firstChild.data
    except Exception as ex:
        pass
        #print 'Error extracting city: %s' % ex
    
    try:
        result['country'] = part.getElementsByTagName('country')[0].firstChild.data
    except Exception as ex:
        #print 'Error extracting country: %s' % ex
        pass
    
    return result
    