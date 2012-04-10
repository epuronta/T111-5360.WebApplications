import re
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_unicode
from api.models import Event

def list_to_json_array(coll):
    arr = '['
    for index, obj in enumerate(coll):
        val = smart_unicode(obj).encode('utf8')
        val = val.replace('\\', '\\\\').replace('"', '\\"')
        val = val.replace('\n', '').replace('\r', '').replace('\t', '')
        if index > 0: arr += ','
        arr += '"%s"' % (val)
        
    arr += ']'
    return arr

def objs_to_json(coll, collname):
    output = '"%s":[' % (collname)
    
    for index, o in enumerate(coll):
	if index  > 0: output += ','
	output += obj_to_json(o)

    output += ']'
    
    return output
    
def obj_to_json(obj):
    output = '{'
    
    #if hasattr(obj, '__dict__'):
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
    #if isinstance(obj, Event) and obj.id:
	#output += ',"uri":"%s"' % (reverse('event-detail-view', args=[obj.id]))
    
    output += '}'
    return output