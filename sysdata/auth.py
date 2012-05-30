#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import json

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=24,error_messages={'required':'Cannot be empty'})
    password = forms.CharField(label='Password', max_length=64,widget=forms.widgets.PasswordInput(),error_messages={'required':'Cannot be empty'})

def login(request):
    redirect_url=request.GET.get('next','/')
    form=LoginForm()
    if request.method=='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request,user)
                    return HttpResponseRedirect(redirect_url)
    return render_to_response('login.html', RequestContext(request,{"form":form,"next":redirect_url}))


def login_ajax(request):
    if request.is_ajax:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return HttpResponse(user.username)
        else:
            # TODO
            pass
            
    
def logout(request):
    auth.logout(request)
    if request.is_ajax:
        return HttpResponse("ok")
    return HttpResponseRedirect("/")

class RegistForm(forms.Form):
    username = forms.CharField(label='Username', max_length=24,
                               error_messages={'required':'Cannot be empty'})
    password = forms.CharField(label='Password', max_length=64,
                               widget=forms.widgets.PasswordInput(),
                               error_messages={'required':'Cannot be empty'})
    confirm = forms.CharField(label='Confirm', max_length=64,
                              widget=forms.widgets.PasswordInput(),
                              error_messages={'required':'Cannot be empty'})
    name = forms.CharField(label='Name', max_length=24,
                           error_messages={'required':'Cannot be empty'})
    email = forms.EmailField(label='E-mail', max_length=24,
                             error_messages={'required':'Cannot be empty'})

#def regist(request):
#    form=RegistForm()
#    if request.method=='POST':
#        form = RegistForm(request.POST)
#        if form.is_valid():
#            username = form.cleaned_data['username']
#            password = form.cleaned_data['password']
#            first_name = form.cleaned_data['name']
#            email = form.cleaned_data['email']
#            user = User.objects.create(username=username,password=password,
#                                       first_name=first_name,email=email)
#            user.save()
#            return HttpResponseRedirect('/')
#    return render_to_response('regist.html', RequestContext(request,{"form":form}))

def regist(request):
    if request.method=='POST':
    #if request.is_ajax():
        #regist_username = request.POST['registname']
        #flag = User.objects.filter(username='allen')
        #if len(flag)==0:
        if request.POST['password']==request.POST['confirm']:
            user = User.objects.create_user(username=request.POST['username'],email=request.POST['email'],
                                            password=request.POST['password'])
            user.save()
            return HttpResponseRedirect('/')
        #else:
            #return HttpResponse('existed') 
    return render_to_response('regist.html',RequestContext(request))