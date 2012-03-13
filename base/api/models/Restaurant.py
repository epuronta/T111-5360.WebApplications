from django.db import models
from django.core.urlresolvers import reverse
import re

class Restaurant(models.Model):
    name = models.CharField(max_length=200,primary_key=True)
    url = models.URLField(max_length=1000)
    info = models.CharField(max_length=1000,blank=True,default='')
    campus = models.CharField(max_length=200)
    street_address = models.CharField(max_length=500)
    lat = models.DecimalField(default=0, max_digits=8, decimal_places=6)
    lon = models.DecimalField(default=0, max_digits=8, decimal_places=6)
    
    class Meta:
	app_label = 'api'