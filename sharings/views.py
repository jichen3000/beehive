# -*- coding: utf-8 -*-
from forms import AddSharingForm  
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
import datetime
from django.core import serializers
from sharings.models import *
from django.db.models import Avg, Max, Min, Count
import json
import Image
from django.core.paginator import Paginator

def index(request):
	hotest_sharings = Sharing.objects.annotate(mediafile_count=Count('mediafile')).filter(
					  edit_status='SHARED',mediafile_count__gt=0).order_by('-updated')[:8]
	tags = Tag.objects.annotate(sharing_count=Count('sharings')).filter(
		   sharing_count__gt=0).order_by('-sharing_count')[:20]
	myfallowed_sharings = None
	if request.user.is_authenticated():				
		myfallowed_sharings = Sharing.objects.filter(followedsharing__follower=request.user).annotate(
							  mediafile_count=Count('mediafile')).filter(
						  	  edit_status='SHARED',mediafile_count__gt=0).order_by('-updated')[:4]	
	return render_to_response('index.html',
							{'hotest_sharings': hotest_sharings,
							'myfallowed_sharings': myfallowed_sharings,
							"tags": tags
							},
							context_instance=RequestContext(request))
	
def get_media_file(file):
	if file:
		media_file = MediaFile(title=file.name, type='PICTURE', file=file, size=file.size)
		return media_file
	return None

def save_tags(tagnamelist, user):
	taglist = []
	for tagname in tagnamelist:
		if tagname != '':
			try:
				tag = Tag.objects.get(name=tagname, created_user=user)
				taglist.append(tag)
			except Tag.DoesNotExist:
				tag = Tag.objects.create(name=tagname, created_user=user)
				taglist.append(tag)
	return taglist

def save_sharing(request, edit_status='UNSHARED'):
	title = request.POST['title']
	content = request.POST['content']
	tagnamelist = request.POST['tags'].split(' ')
	sharingid = request.POST['sharingid']
	user = request.user
	if sharingid:
		sharing = Sharing.objects.get(pk=sharingid)
	else:
         sharing = Sharing.objects.create(author=user)
	sharing.content = content
	sharing.title = title
	sharing.tags = save_tags(tagnamelist, user)
	sharing.edit_status = edit_status
	sharing.save()
	return sharing
	
def medias_auto_save(request):
    if request.method == 'POST':
        form = AddSharingForm(request.POST, request.FILES)
        if form.is_valid():
			sharing = save_sharing(request)
			media_file = get_media_file(request.FILES['file'])
			if media_file:
			    sharing.mediafile_set.add(media_file)
			sharing.save()
			data = {'filename': media_file.file.name, 'sharingid':sharing.id , 'mediafileid':media_file.id, 'aspectratio':media_file.is_over_16_9()}
			return HttpResponse(json.dumps(data))
    else:
        return HttpResponse(status=400)
       
def ajax_add_sharing(request):
	if request.is_ajax():
		sharing = save_sharing(request)
		return HttpResponse(sharing.id)
	else:
		return HttpResponse(status=400)
	
def ajax_delete_mediafile(request):
	if request.is_ajax():
		mediafileid = request.POST['mediafileid']
		if mediafileid:
			mediafile = MediaFile.objects.get(pk=mediafileid)
			mediafile.delete()
			return HttpResponse("success")
	else:
		return HttpResponse(status=400)
		
def add_sharing(request):
    if request.method == 'POST':
        form = AddSharingForm(request.POST, request.FILES)
        if form.is_valid(): 
			sharing = save_sharing(request, 'SHARED')
			return HttpResponseRedirect(reverse('sharings.views.detail', args=(sharing.id,)))
    else:
        form = AddSharingForm()
    return render_to_response('sharing_add.html', {'form':form}, context_instance=RequestContext(request))
    
def detail(request, sharing_id):
	sharing = get_object_or_404(Sharing, pk=sharing_id)
	tags = Tag.objects.annotate(sharing_count=Count('sharings')).filter(
		sharing_count__gt=0).order_by('-sharing_count')[:20]
	is_followed = request.user.is_anonymous() or FollowedSharing.objects.filter(followed_sharing=sharing, follower=request.user).exists()
	sharing.voted_value = 0 # no voted
	if request.user.is_authenticated():
		sharingVotingSet = SharingVoting.objects.filter(sharing=sharing, voter=request.user)
		if sharingVotingSet:
			sharing.voted_value = sharingVotingSet[0].value
	resharings = [_set_vote_value(resharing, request) for resharing in sharing.resharings.all()]
	return render_to_response('sharing_detail.html', 
								{'sharing': sharing, "tags": tags, "resharings": resharings, "is_followed": is_followed}, 
								context_instance=RequestContext(request))
    
def _set_vote_value(sharing, request):
	sharing.voted_value = 0 # no voted
	if request.user.is_authenticated():
		sharingVotingSet = SharingVoting.objects.filter(sharing=sharing, voter=request.user)
		if sharingVotingSet:
			sharing.voted_value = sharingVotingSet[0].value
	return sharing

def add_comment(request, sharing_id):
	if request.is_ajax():
		sharing = get_object_or_404(Sharing, pk=sharing_id)
		c = Comment(author=request.user, commented_sharing=sharing, content=request.POST['commentContent'])
		c.save()
		return HttpResponse(serializers.serialize('json', [c, c.author]))
	else:
		# TODO
		pass
	
def get_most_used_tag_list():
	# tags sharing count > 0 and order by sharing count
	return Tag.objects.annotate(sharing_count=Count('sharings')).filter(
								sharing_count__gt=0).order_by('-sharing_count')[:20]

def get_sharings_paginator():
	sharings_all_list = Sharing.objects.annotate(mediafile_count=Count('mediafile')).filter(edit_status='SHARED',
		mediafile_count__gt=0).order_by('-updated')
	return Paginator(sharings_all_list, 10)


def list_sharings(request, title):
	sharings_paginator = get_sharings_paginator()
	sharings_list = sharings_paginator.page(1).object_list
	tags = get_most_used_tag_list()
	return render_to_response("sharing_list.html", 
							{"title": title, "sharings_list":sharings_list,
							"num_pages":sharings_paginator.num_pages,"tags": tags},
							context_instance=RequestContext(request))
	
	
def load_more_sharings(request):
	sharings_paginator = get_sharings_paginator()
	if request.is_ajax():
		page_index=int(request.GET.get('page',1))
		sharings_list=None
		if page_index<=sharings_paginator.num_pages:
			sharings_list = sharings_paginator.page(page_index).object_list
		return render_to_response("include/_sharing_list_content.html", 
								{"sharings_list": sharings_list},
								context_instance=RequestContext(request))
	else:
		return HttpResponse(status=400)
	
	
def all_sharings(request):
	return list_sharings(request, "All")

def hotest_sharings(request):
	hotest_sharings_paginator = get_sharings_paginator()
	sharings_list = hotest_sharings_paginator.page(1).object_list
	tags = get_most_used_tag_list();
	if request.is_ajax():
		return render_to_response("include/_new_sharing_list_content.html", 
								{"sharings_list": sharings_list},
								context_instance=RequestContext(request))
	else:
		return render_to_response("sharing_list.html", 
								{"title": "Hottest","num_pages":hotest_sharings_paginator.num_pages, 
								"sharings_list":sharings_list,"tags": tags},
							context_instance=RequestContext(request))
	
def myfollow_sharings(request):
	sharings_list = Sharing.objects.filter(followedsharing__follower=request.user).annotate(mediafile_count=Count('mediafile')).filter(edit_status='SHARED',
		mediafile_count__gt=0).order_by('-updated')
	
	# tags sharing count > 0 and order by sharing count
	tags = get_most_used_tag_list();
	if request.is_ajax():
		return render_to_response("include/_new_sharing_list_content.html", 
								{"sharings_list": sharings_list},
								context_instance=RequestContext(request))
	else:
		return render_to_response("sharing_list.html", {"sharings_list": sharings_list, "title": "My Followed", "tags": tags},
								context_instance=RequestContext(request))

def tag_sharings(request, tag_id):
	tag = get_object_or_404(Tag, pk=tag_id)
	sharings = tag.sharings.all()
	tags = get_most_used_tag_list()
	return render_to_response("sharing_list.html",
							{"sharings": sharings, "title": "Tagged Sharings: \" %s \"" % tag.name, "tags": tags},
							context_instance=RequestContext(request))


def vote(request, sharing_id, vote_value):
	vote_value = int(vote_value)
	if request.is_ajax():
		sharing = get_object_or_404(Sharing, pk=sharing_id)
		vote = SharingVoting(sharing=sharing, voter=request.user, value=vote_value)
		vote.save()
		sharingData, created = SharingData.objects.get_or_create(sharing=sharing)
		if vote_value == 1:
			sharingData.plus_voting_count += 1
			count = sharingData.plus_voting_count
		elif vote_value == -1:
			sharingData.minus_voting_count += 1
			count = sharingData.minus_voting_count
		else:
			# TODO
			return
		sharingData.save()
		return HttpResponse(json.dumps({"count": count}))
	else:
		# TODO
		pass
	
def follow(request, sharing_id):
	if request.is_ajax():
		sharing = get_object_or_404(Sharing, pk=sharing_id)
		followedSharing, followed = FollowedSharing.objects.get_or_create(followed_sharing=sharing, follower=request.user)
		sharingData, created = SharingData.objects.get_or_create(sharing=sharing)
		if followed:#a new follow
			sharingData.follow_count += 1 
		else:
			followedSharing.delete()
			sharingData.follow_count -= 1 
		sharingData.save()
		return HttpResponse(json.dumps({"count": sharingData.follow_count}))
	else:
		# TODO
		pass
		
def new_version(request):
	sharings_list = Sharing.objects.annotate(mediafile_count=Count('mediafile')).filter(edit_status='SHARED',
		mediafile_count__gt=0).order_by('-updated')[:10]
	tags = get_most_used_tag_list()
	return render_to_response("new_sharing_list.html", {"sharings_list":sharings_list,"tags": tags},
							context_instance=RequestContext(request))
	
	
def report(request):
	return render_to_response("sharing_report.html", 
							context_instance=RequestContext(request))
	
def brand_keywords(brand):
	data=None
	if brand=="Coca-Cola":
		data={'Coca-Cola':9500,'Coca-Cola Company': 10502,  'Fruitopia': 9598,
				  'Surge': 5500,'root beer': 1638,'Minute Maid':4000}
	elif brand=="Pepsi":
		data={'Pepsi':8500,'Pepsi Cola': 11502,  'Caleb Bradham': 9998,
				  'QIXi': 5507,'Pepsico.': 6783,'Tricon Global':4593,'JiLang':10000}
	elif brand=="KangShiFu":
		data={'KangShiFu tea':9500,'KangShiFu water': 1512,  'KangShiFu red tea': 7998,
				  'KangShiFu green tea': 5507,'KangShiFu Orange': 6784,'KangShiFu':4593}
	else :
		data={'RedBull':10000,'Nestle':10000,'TongYi':10000,'Wahaha':10000,'WangLaoJi':10000}
	return data

def keywords_analysis(request):
	if request.is_ajax():
		brand=request.POST['brand']
		data=brand_keywords(brand)
		return HttpResponse(json.dumps(data)) 
	else:
		return HttpResponse(status=400)

def manafactuser(request):
    return hotest_sharings(request)
   
def list_comments(request, sharing_id):
	comments = Comment.objects.filter(commented_sharing=Sharing(id=sharing_id))
	if request.is_ajax():
		return render_to_response("include/_new_sharing_comments.html", 
								{"comments": comments},
								context_instance=RequestContext(request))

