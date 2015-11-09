# -*- coding: utf-8 -*-
from django.db import models

# TODO to be relpaced with your own domain name
DOMAIN_ROOT = "hackit.cn"
class Subdomain(models.Model):
    subdomain = models.CharField(max_length=32, default="sample", blank=True, null=True)
    campus_name_en = models.CharField(max_length=128, blank=True, null=True)
    weight = models.IntegerField(default=0, blank=True, null=True)
    to_delete = models.BooleanField(default=False, verbose_name="删除站点")
    to_create = models.BooleanField(default=True, verbose_name="新建或重新部署")
    campus_name_cn = models.CharField(max_length=256, blank=True, null=True)
    description = models.CharField(max_length=1024, blank=True, null=True)
    address = models.CharField(max_length=128, blank=True, null=True)
    fax = models.CharField(max_length=32, blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    logo_url = models.CharField(max_length=128, blank=True, null=True)
    domain = models.CharField(max_length=32, default="", blank=True, null=True, verbose_name="Index Url")

    def __unicode__(self):
        return self.subdomain
