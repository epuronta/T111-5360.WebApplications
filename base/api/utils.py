import re

def events_to_json(events):
    output = ''
    
    for event in events:
	output += obj_to_json(event)
	
    return output
    
def obj_to_json(obj):
    output = '{'
    
    for attr in obj.__dict__:
	if re.match('_', attr):
	    continue
	output += '%s:"%s",' % (attr, obj.__dict__[attr])
	
    output += '}'
    return output