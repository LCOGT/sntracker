from __future__ import unicode_literals

from django.db import models
from datetime import datetime

STATUS_CHOICES = (
                ('P','Pending'),
                ('C','Completed'),
                ('S','Scheduled'),
                ('N','Canceled'),
                ('F','Failed')
                )

SCOPE_CHOICES = (
                ('0m4','0.4-meter'),
                ('1m0','1.0-meter'),
                ('2m0','2.0-meter')
                )

INSTRUMENT_CHOICES = (
("1M0-SCICAM-SBIG", '1m Science Camera'), ("1M0-SCICAM-SINISTRO", 'Sinistro'), ('2M0-SCICAM-SPECTRAL', 'Spectral'), ('2M0-SCICAM-MEROPE', 'Merope')
)

FILTER_CHOICES = (
                ('Ha', 'H-alpha'),
                ('D51', 'D51'),
                ('H-Beta', 'H Beta'),
                ('OIII', 'OIII'),
                ('H-Alpha', 'H Alpha'),
                ('Skymapper-VS', 'Skymapper CaV'),
                ('solar', 'Solar (V+R)'),
                ('Astrodon-UV', 'Astrodon UV'),
                ('I', 'Bessell-I'),
                ('R', 'Bessell-R'),
                ('U', 'Bessell-U'),
                ('w', 'PanSTARRS-w'),
                ('Y', 'PanSTARRS-Y'),
                ('up', 'SDSS-u&prime;'),
                ('air', 'Clear'),
                ('rp', 'SDSS-r&prime;'),
                ('ip', 'SDSS-i&prime;'),
                ('gp', 'SDSS-g&prime;'),
                ('zs', 'PanSTARRS-Z'),
                ('V', 'Bessell-V'),
                ('B', 'Bessell-B'),
                ('clear', 'clear')
                 )

class Supernova(models.Model):
    name                = models.CharField('Designation',max_length=15, blank=True, null=True)
    start               = models.DateTimeField(blank=True, null=True)
    end                 = models.DateTimeField(blank=True, null=True)
    information         = models.TextField(blank=True, null=True)
    teaser              = models.CharField(max_length=120)
    image               = models.CharField(max_length=50, default="no-image.jpg")
    timelapse_url       = models.URLField(blank=True, null=True)
    num_observations    = models.IntegerField(default=0,blank=True, null=True)
    last_update         = models.DateTimeField(blank=True, null=True)
    active              = models.BooleanField(default=True)
    ra                  = models.FloatField(default=0.0)
    dec                 = models.FloatField(default=0.0)

    def text_name(self):
        return self.name.replace(" ","_")

    def __unicode__(self):
        return self.name

class Exposure(models.Model):
    filter_name         = models.CharField(max_length=30, choices=FILTER_CHOICES)
    repeats             = models.IntegerField(default=0)
    supernova           = models.ForeignKey(Supernova)
    aperture            = models.CharField(max_length=4, choices=SCOPE_CHOICES)
    instrument          = models.CharField(max_length=20, choices=INSTRUMENT_CHOICES)
    exposure_time       = models.FloatField(default=0.0)

class Observation(models.Model):
    track_num           = models.CharField(max_length=10)
    status              = models.CharField(max_length=1, choices=STATUS_CHOICES)
    last_update         = models.DateTimeField(blank=True, null=True)
    email               = models.CharField('Email address of the submitter', max_length=150, blank=True, null=True)
    supernova           = models.ForeignKey(Supernova)
    request_ids         = models.TextField(blank=True, null=True)
    frame_ids           = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return "%s for %s is %s" % (self.track_num, self.email, self.status)
