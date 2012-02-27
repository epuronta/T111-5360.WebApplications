import re
from django.core.urlresolvers import reverse
from models import Event

def events_to_json(events):
    output = '{events:['
    
    for event in events:
	output += obj_to_json(event)
	output += ','

    output += ']}'
    return output
    
def obj_to_json(obj):
    output = '{'
    # Loop through object attributes
    for attr in obj.__dict__:
	if re.match('_', attr): # Ignore prefixed with _
	    continue
	# Add the rest as name:"value" pairs
	output += '%s:"%s",' % (attr, obj.__dict__[attr])

    # Class-specific encodings
    if isinstance(obj, Event) and obj.id:
	output += 'uri:"%s",' % (reverse('event-detail-view', args=[obj.id]))
    
    output += '}'
    return output