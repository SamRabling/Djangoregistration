from __future__ import unicode_literals
from django.shortcuts import render, redirect
from models import *
import bcrypt
from django.contrib import messages

def index(request):
    print "index engaged"
    context={
        'users':User.objects.all()
    }
    return render(request,"belt/index.html", context)

def create(request):
    print "create engaged"
    errors = User.objects.regis_basic_validator(request.POST)
    print "create processing"
    if len(errors):
        for tag, errors in errors.iteritems():
            messages.error(request, errors, extra_tags=tag)
            return redirect('/')
    print "create processing..."
    passworD = request.POST['Password']
    hashed = bcrypt.hashpw(passworD.encode(),bcrypt.gensalt())
    if request.method == "POST":
        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hashed)
        print "new id created"
        request.session['id'] = user.id
        return redirect('/success')

def process(request):
    print "process engaged"
    erros = User.objects.log_basic_validator(request.POST)
    if len(errors):
        for tag, errors in errors.iteritems():
            messages.error(request, errors, extra_tags=tag)
            return redirect('success')
    request.session['id'] = user.id
    print "validation in process"

def success(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        context = {
	    	'first_name': User.objects.get(id=request.session['id']).first_name
	    }
        print "success engaged"
        return render(request,"belt/success.html", context)

def loggout(request):
    request.session.clear()
    return redirect('/')


def update(request):
    response="yo dawg, it's me update!"
    return HttpResponse(response)

def destroy(request):
    response="yo dawg, it's me destroy!"
    return HttpResponse(response)




  


