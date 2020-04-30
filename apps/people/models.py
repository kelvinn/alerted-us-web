from django.contrib.gis.db import models
from django.contrib.auth.models import User
from apps.alertdb.models import Info
from django.db.models import Manager as GeoManager


class Location(models.Model):
    LOCATION_SOURCE = (
        ('static', 'Static'),
        ('current', 'Current Location'),
    )
    user = models.ForeignKey(User, editable=True, on_delete=models.CASCADE)
    date_received = models.DateTimeField(auto_now=True)
    name = models.TextField(blank=True, null=True)
    source = models.CharField(max_length=50, blank=True, null=True, choices=LOCATION_SOURCE)
    geom = models.PointField(blank=True, null=True, srid=4326)
    objects = GeoManager()

    def __unicode__(self):
        return str(self.name)


class LocationHistory(models.Model):
    user = models.ForeignKey(User, editable=True, on_delete=models.CASCADE)
    date_received = models.DateTimeField(auto_now_add=True)
    name = models.TextField(blank=True, null=True)
    geom = models.PointField(blank=True, null=True, srid=4326)
    objects = GeoManager()

    def __unicode__(self):
        return str(self.name)

