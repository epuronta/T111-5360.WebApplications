from django.db import models
from django.core.urlresolvers import reverse
import re

WEEKDAYS = [
  (1, ("Monday")),
  (2, ("Tuesday")),
  (3, ("Wednesday")),
  (4, ("Thursday")),
  (5, ("Friday")),
  (6, ("Saturday")),
  (7, ("Sunday")),
]
    
class OpeningHours(models.Model):
    restaurant = models.ForeignKey("Restaurant")
    weekday = models.IntegerField(choices=WEEKDAYS)
    from_hour = models.IntegerField()
    to_hour = models.IntegerField()

    def get_weekday_display(self):
        return WEEKDAYS[self.weekday]

    class Meta:
	app_label = 'api'