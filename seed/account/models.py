# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractUser
from globe.utils import update_uploaded_filename

from redactor.fields import RedactorField
import time
import base64

# model for liuxue wiki account
class WikiUser(AbstractUser):
    PRIVILEGES = (
        ('NORMAL', 'Normal users'),
        ('EDITOR', 'Wiki editors'),
        ('SUPER', 'Super users'),
    )

    head_icon = models.FileField(upload_to=update_uploaded_filename, blank=True, null=True)
    nickname = models.CharField(max_length=128, default='NickName', blank=True, null=True)
    campus_name = models.CharField(max_length=128, default='', blank=True, null=True)
    status = models.CharField(max_length=128, default='我爱我的范', blank=True, null=True)
    hometown = models.CharField(max_length=128, default='', blank=True, null=True)
    kaopu_value = models.IntegerField(default=0, blank=True, null=True)
    bukaopu_value = models.IntegerField(default=0, blank=True, null=True)
    contrib_value = models.IntegerField(default=0, blank=True, null=True)
    age = models.IntegerField(default=0, blank=True, null=True)

    facebook_link = models.CharField(max_length=128, default='', blank=True, null=True)
    twitter_link = models.CharField(max_length=128, default='', blank=True, null=True)
    linkedin_link = models.CharField(max_length=128, default='', blank=True, null=True)
    weibo_link = models.CharField(max_length=128, default='', blank=True, null=True)
    renren_link = models.CharField(max_length=128, default='', blank=True, null=True)
    
    privilege = models.CharField(max_length=16, blank=True, default='NORMAL', choices=PRIVILEGES)

    backup_email = models.CharField(max_length=128, default='', blank=True, null=True)
    checked = models.BooleanField(default=False)
    link_expire_time = models.DateTimeField(blank=True, null=True)
    check_string = models.CharField(max_length=512, default='', blank=True, null=True)

    unread_cnt = models.IntegerField(default=0)
    major = models.CharField(max_length=64, default='', blank=True, null=True)
    minor = models.CharField(max_length=64, default='', blank=True, null=True)


    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"
 
    def save(self, *args, **kwargs):
        c_str = base64.b64encode(self.email + time.strftime('%m/%d/%Y%H:%M:%S'))
        self.check_string = c_str
        super(WikiUser, self).save(*args, **kwargs)

# model 
class Message(models.Model):
    title = models.CharField(max_length=128, blank=True, null=True, default='站内信标题')
    sender = models.ForeignKey(WikiUser, blank=True, null=True, related_name="messages_sent")    
    receiver = models.ForeignKey(WikiUser, blank=True, null=True, related_name="messages_received")
    read = models.BooleanField(default=False)
    content = RedactorField(
        blank=True,
        null=True,
        verbose_name=u'Message',
        redactor_options={'lang':'zh_cn', 'focus':'true'},
    )
    timestamp = models.DateTimeField(auto_now_add=True)
     
class Major(models.Model):
    user = models.ForeignKey(WikiUser, related_name="majors")
    major = models.CharField(max_length=128, blank=True, null=True, default='')

class Minor(models.Model):
    user = models.ForeignKey(WikiUser, related_name="minors")
    minor = models.CharField(max_length=128, blank=True, null=True, default='')
    
