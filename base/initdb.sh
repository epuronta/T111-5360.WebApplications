#!/bin/sh
rm maindb.sqlite
python manage.py syncdb
#python manage.py generate_debug_events 20
python manage.py fetch_aalto_events
python manage.py fetch_lunch
