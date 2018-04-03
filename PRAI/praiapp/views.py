from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from models import Signup
# Create your views here.
def signup(request):
	if request.method == 'GET':
		signup=Signup()
		print signup.name
		return render(request,"signup.html",{})
	elif request.method == 'POST':
		signup=Signup()
		value=0
		print "requesmethod",request.method
		name=request.POST.get("name" or None)
		if name is None or '' or len(name)==0:
			print "name"
			value=1
		print "len name",len(name)
		email=request.POST.get("email" or None)
		if email== None or '@' not in email:
			print "email"
			value=2
		passwd=request.POST.get("passwd" or None)
		if passwd== None or len(passwd)<8:
			print "passwd"
			value=3
		exist=Signup.objects.filter(name=name)
		if len(exist)>0 and value!=1:
			value=4
		print value
		if value==1:
			return render(request,"signup.html",{'noname':True})
		elif value==2:
			return render(request,"signup.html",{'noemail':True})
		elif value==3:
			return render(request,"signup.html",{'nopasswd':True})
		elif value==4:
			return render(request,"signup.html",{'existing':True})
		p=Signup(name=name,email=email,passwd=passwd)
		p.save()
		return render(request,"signup.html",{})

def login(request):
	if request.method=='GET':
		return render(request,"login.html",{})
	elif request.method=='POST':
		username=request.POST.get("name")
		password=request.POST.get("passwd")
		print username,password
		try:
			signedname=Signup.objects.get(name=username)
			print signedname.passwd
			if str(signedname.passwd) == str(password):
				request.session['member_id']=signedname.id
				print "sesion is for",request.session['member_id']
				return HttpResponseRedirect('/userlogin/')
			else:
				return render(request,"login.html",{'invalid':True})# -*- coding: utf-8 -*-
		except:
			return render(request,"login.html",{'there':True})



def userlogin(request):
	if request.method == 'GET':
		userid=request.session['member_id']
		print "userid",userid
		signupobj=Signup.objects.get(id=userid)
		name=signupobj.name
		return render(request,"userlogin.html",{'name':name})

def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return render(request,"logout.html",{})

def home(request):
	return render(request,"home.html",{})


def sentiment(request):
	token=request.GET.get("access_token")
	print token
	return HttpResponseRedirect('/sentiment/')

def demo(request):
	return HttpResponse('THANKS')


def wordpress(request):
	return render(request,"sentiment.html",{})