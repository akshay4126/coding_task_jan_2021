from django.db import models
# Create your models here.
from sentiance.settings import VisitLabels
#def lat_lon_2gcode(latitude,longitude):


class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    level = models.IntegerField()
    gcode = models.CharField(max_length=32)

    def __str__(self):
        return self.gcode


class Person(models.Model):
    person_id = models.CharField(max_length=255)

    def __str__(self):
        return self.person_id


class Visit(models.Model):
    person = models.ForeignKey(Person, related_name="visits",
                               on_delete=models.CASCADE)
    location = models.ForeignKey(Location, related_name="visits",
                                 on_delete=models.CASCADE)
    visit_count = models.IntegerField(default=0)
    visit_label = models.CharField(max_length=128, default=VisitLabels.VISIT_UNKNOWN.value)

    def __str__(self):
        return '{} visited the location "{}", {} times'.format(self.person, self.location, self.visit_count)
