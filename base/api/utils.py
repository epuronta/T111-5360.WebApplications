import re
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_unicode
from api.models import Event

def objs_to_json(coll, collname):
    output = '"%s":[' % (collname)
    
    for index, o in enumerate(coll):
	if index  > 0: output += ','
	output += obj_to_json(o)

    output += ']'
    
    return output
    
def obj_to_json(obj):
    output = '{'
        
    # Loop through object attributes
    for index, attr in enumerate(obj.__dict__):
	if re.match('_', attr): # Ignore prefixed with _
	    continue
	# Add the rest as name:"value" pairs
	if index > 0: output += ','
	dataval = obj.__dict__[attr]
        dataval = smart_unicode(dataval).encode('utf8')
	dataval = dataval.replace('\\', '\\\\').replace('"', '\\"')
	dataval = dataval.replace('\n', '').replace('\r', '').replace('\t', '')
	output += '"%s":"%s"' % (attr, dataval)

    # Class-specific urls
    if isinstance(obj, Event) and obj.id:
	output += ',"uri":"%s"' % (reverse('event-detail-view', args=[obj.id]))
    
    output += '}'
    return output