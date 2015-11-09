# -*- coding: utf-8 -*-
import datetime
from django.db import models

from redactor.fields import RedactorField
from account.models import WikiUser
from globe.utils import update_uploaded_filename

import os
from django.conf import settings
# Tags, one tags relates with many entries
class Tag(models.Model):
    tag = models.CharField(max_length=128, blank=False, unique=True)    
    def __unicode__(self):
        return self.tag

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'
        
class Entry(models.Model):
    title = models.CharField(max_length=250, default="Title", blank=True, null=True, verbose_name=u'Title')
    content = RedactorField(
        blank=True,
        null=True,
        verbose_name=u'Content',
        redactor_options={'lang': 'zh_cn', 'focus': 'true'},
    )
    
    creator = models.ForeignKey(WikiUser, related_name="created_entries")
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)
    pass_audit = models.BooleanField(default=False)
    view_cnt = models.IntegerField(default=0)
    time_stamp = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)
    ver_time = models.DateTimeField(blank=True, null=True)
    
    saved = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = '词条'
        verbose_name_plural = '词条'

    def __unicode__(self):
        return self.title

class EditAction(models.Model):
    editor = models.ForeignKey(WikiUser, related_name="edit_history")
    entry = models.ForeignKey(Entry, related_name="change_history")
    time_stamp = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=256, blank=True, null=True, default="Content Changed")
        
class HotTag(models.Model):
    tag = models.ForeignKey(Tag)        
    description = models.CharField(max_length=512, blank=True, null=True, default="Hot Tag!")
    time_stamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '热门标签'
        verbose_name_plural = '热门标签'

class ViewMost(models.Model):
    entry = models.ForeignKey(Entry)
    description = models.CharField(max_length=512, blank=True, null=True, default="Hot!")
    time_stamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "最热词条"
        verbose_name_plural = "最热词条"
        
class KaopuMost(models.Model):
    entry = models.ForeignKey(Entry)
    description = models.CharField(max_length=512, blank=True, null=True, default="Kaopu!")
    time_stamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "最靠谱词条"
        verbose_name_plural = "最靠谱词条"

class RecentMost(models.Model):
    entry = models.ForeignKey(Entry)
    description = models.CharField(max_length=512, blank=True, null=True, default="Recent!")
    time_stamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "最新词条"
        verbose_name_plural = "最新词条"

class NiuMost(models.Model):
    editor = models.ForeignKey(WikiUser)
    description = models.CharField(max_length=512, blank=True, null=True, default="Niu!")
    time_stamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "最牛编辑者"
        verbose_name_plural = "最牛编辑者"

class Attachments(models.Model):
    entry = models.ForeignKey(Entry, related_name="attachments")
    filename = models.CharField(max_length=128, blank=True, null=True)
    url = models.CharField(max_length=512, blank=True, null=True)
    def save(self, *args, **kwargs):
        media_url = getattr(settings, 'MEDIA_URL', '/media/')
        self.url = media_url + "attach/"+str(self.entry.pk)+"/"+self.filename
        super(Attachments, self).save(*args, **kwargs)
