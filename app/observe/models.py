from __future__ import unicode_literals

from django.db import models
from datetime import datetime

from astropy.time import Time


STATUS_CHOICES = (
                ('P','Pending'),
                ('C','Completed'),
                ('S','Scheduled'),
                ('N','Canceled'),
                ('F','Failed')
                )

class Supernova(models.Model):
    name                = models.CharField('Designation',max_length=15, blank=True, null=True)
    filter_name         = models.CharField(max_length=10)
    exposure_count      = models.IntegerField(default=1)
    start               = models.DateTimeField(blank=True, null=True)
    end                 = models.DateTimeField(blank=True, null=True)
    information         = models.TextField(blank=True, null=True)
    teaser              = models.CharField(max_length=120)
    image               = models.CharField(max_length=50, default="no-image.jpg")
    timelapse_url       = models.URLField()
    num_observations    = models.IntegerField(default=0)
    last_update         = models.DateTimeField(blank=True, null=True)

    def text_name(self):
        return self.name.replace(" ","_")

    def __unicode__(self):
        return self.name

class Filter(models.Model):
    name                = models.CharField(max_length=30)
    repeats             = models.IntegerField(default=0)
    supernova           = models.ForeignKey(Supernova)
    aperture            = models.CharField(max_length=4)

class Observation(models.Model):
    track_num           = models.CharField(max_length=10)
    status              = models.CharField(max_length=1, choices=STATUS_CHOICES)
    last_update         = models.DateTimeField(blank=True, null=True)
    email               = models.CharField(max_length=150, blank=True, null=True)
    supernova           = models.ForeignKey(Supernova)
    request_ids         = models.TextField(blank=True, null=True)
    frame_ids           = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return "%s for %s is %s" % (self.track_num, self.email, self.status)
