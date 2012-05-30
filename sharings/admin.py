#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from sharings.models import *


admin.site.register(Sharing)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(MediaFile)
admin.site.register(UserProfile)
admin.site.register(FollowedSharing)
admin.site.register(SharingData)
admin.site.register(SharingVoting)

