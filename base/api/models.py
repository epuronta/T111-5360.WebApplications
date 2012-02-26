from django.db import models
from django.core.urlresolvers import reverse
import re

class Event(models.Model):
    title = models.CharField(max_length=200)
    descr = models.TextField()

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    street_address = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    country = models.CharField(max_length=100)
    
    lat = models.DecimalField(default=0, max_digits=8, decimal_places=6)
    lon = models.DecimalField(default=0, max_digits=8, decimal_places=6)

    org_name = models.CharField(max_length=100)
    org_email = models.EmailField()
    org_phone = models.CharField(max_length=100)