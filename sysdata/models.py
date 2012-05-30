# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Parameter(models.Model):
    name = models.CharField(max_length=30)
    value = models.CharField(max_length=30)
    # INT, STRING
    type = models.CharField(max_length=30)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True,auto_now=True)

    def __unicode__(self):
        return self.name
    
class ActionLog(models.Model):
    user = models.ForeignKey(User)
    url = models.CharField(max_length=255)
    ip_address = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True,auto_now=True)
    
    def __unicode__(self):
        return self.url
    