# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
import json
import Image

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True,auto_now=True)


class Tag(models.Model):
    created_user = models.ForeignKey(User)
    name = models.CharField(max_length=20)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True,auto_now=True)
    
    def __unicode__(self):
		return self.name
    

class Sharing(models.Model):
    author = models.ForeignKey(User)
    parent_sharing = models.ForeignKey('self',related_name='resharings',blank=True,null=True)
    followed_users = models.ManyToManyField(User, related_name='followed_sharings',blank=True)
    tags = models.ManyToManyField(Tag, related_name='sharings', blank=True)
    title = models.CharField(max_length=30,blank=True,null=True)
    content = models.CharField(max_length=500,blank=True,null=True)
    #UNSHARED, SHARED
    edit_status = models.CharField(max_length=30)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True,auto_now=True)
    
    def __unicode__(self):
		return self.title  
	
    def get_mediafile_path_liststr(self):
        mediafiles = []
        for mediafile in self.mediafile_set.all():
          mediafiles.append({"name": mediafile.file.name,"is_over_16_9":mediafile.is_over_16_9()})
        result = json.dumps(mediafiles)
        return result
	   
	
class FollowedSharing(models.Model):
    followed_sharing = models.ForeignKey(Sharing)
    follower = models.ForeignKey(User)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True,auto_now=True)
    
    def __unicode__(self):
        return self.followed_sharing.title
    
class Comment(models.Model):
    author = models.ForeignKey(User)
    commented_sharing = models.ForeignKey(Sharing)
    content = models.CharField(max_length=500)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True,auto_now=True)

    def __unicode__(self):
        return self.content
    

class TagRecord(models.Model):
    performer = models.ForeignKey(User)
    tag = models.ForeignKey(Tag)
    created_sharing_count = models.IntegerField(blank=True)
    created_comment_count = models.IntegerField(blank=True,null=True)
    follow_count = models.IntegerField(blank=True)
    focus_count = models.IntegerField(blank=True)
    scores = models.IntegerField(blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True,auto_now=True)

    def __unicode__(self):
        return self.tag.name
    
class MediaFile(models.Model):
    sharing = models.ForeignKey(Sharing)
    title = models.CharField(max_length=20) 
    file = models.FileField(upload_to='share_media/pics/%Y/%m/%d')
    thumbnail = models.FileField(upload_to='share_media/pics/%Y/%m/%d',
                                 blank=True,null=True)
    # PICTURE, VIDEO, AUDIO
    type = models.CharField(max_length=30)
    size = models.IntegerField()
    
    height_px = models.IntegerField(blank=True,null=True)
    width_px = models.IntegerField(blank=True,null=True)
    width_height_rate = models.FloatField(blank=True,null=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True,auto_now=True)

    def __unicode__(self):
        return self.file.path

    def save(self):
        im = Image.open(self.file)
#        self.width_px = 100
        self.width_px,self.height_px = im.size
        self.width_height_rate = round(float(self.width_px)/self.height_px,2)
        super(MediaFile, self).save()
    def is_over_16_9(self):
    	return self.width_height_rate > 1.77
	
	
	
class SharingData(models.Model):
    sharing = models.OneToOneField(Sharing, related_name='sharing_data')
    plus_voting_count = models.IntegerField(default=0)
    minus_voting_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    follow_count = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.sharing.title
    
class SharingVoting(models.Model):
    sharing = models.ForeignKey(Sharing)
    voter = models.ForeignKey(User)
    
    value = models.IntegerField()
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True,auto_now=True)
    
    def __unicode__(self):
        return self.sharing.title+", "+self.voter.username


    