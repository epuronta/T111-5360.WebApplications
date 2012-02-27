#!/bin/sh
rm maindb.sqlite
python manage.py syncdb
python manage.py generate_debug_events 20
