# -*- coding: utf-8 -*-
from django.db import models
from globe.utils import upload_logo
from globe.utils import upload_corner
from globe.utils import upload_background
from globe.utils import OverwriteStorage

class University(models.Model):
    campus_name_en = models.CharField(max_length=128, blank=True, null=True)
    campus_name_zh = models.CharField(max_length=256, blank=True, null=True)
    email_suffix = models.CharField(max_length=64, blank=True, null=True)
    description = models.CharField(max_length=1024, blank=True, null=True)
    address = models.CharField(max_length=128, blank=True, null=True)
    fax = models.CharField(max_length=32, blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    corner_logo = models.FileField(upload_to=upload_corner, storage=OverwriteStorage(), blank=True, null=True)
    logo = models.FileField(upload_to=upload_logo,storage=OverwriteStorage(), blank=True, null=True)
    background = models.FileField(upload_to=upload_background, storage=OverwriteStorage(), blank=True, null=True)

    def __unicode__(self):
        return self.campus_name_en

