from __future__ import unicode_literals
from django.shortcuts import render, redirect
from models import *
import bcrypt
from django.contrib import messages

## ---------------- LOGIN AND REGISTRATION --------
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
        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], birthday=request.POST['birthday'], password=hashed)
        print "new id created"
        request.session['id'] = user.id
        return redirect('/dashboard')

def process(request):
    print "process engaged"
    errors = User.objects.log_basic_validator(request.POST)
    if len(errors):
        for tag, errors in errors.iteritems():
            messages.error(request, errors, extra_tags=tag)
            print "validation in process"
            return redirect('/')
    email = request.POST['email']
    request.session['id'] = User.objects.get(email=email).id
    print User.objects.get(email=email).id
    print "validation in process"
    return redirect('/dashboard')

## -------------------- PAGES ----
def index(request):
    print "index engaged"
    context={
        'users':User.objects.all()
    }
    return render(request,"belt/index.html", context)

def dashboard(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id = request.session['id'])
        item = Item.objects.all()
        context = {
	    	'first_name': User.objects.get(id=request.session['id']).first_name,
            'item': item
	    }
        print "dashboard engaged"
        return render(request,"belt/dashboard.html", context)
    
def wished(request):
    if 'id' not in request.session:
        return redirect('/')
    # errors = Item.objects.item_basic_validator(request.POST)
    # if len(errors):
    #     for tag, errors in errors.iteritems():
    #         messages.error(request, errors, extra_tags=tag)
    #         print "validation in process"
    #         request.session['id'] = User.objects.get(email=email).id
    #         return redirect('wished_items/create')

    # context = {
    #     name = User.objects.get(id=request.session['id']).first_name
    # }
    
    return render(request,"belt/add.html")

def item(request):
    if 'id' not in request.session:
        return redirect('/')
    return render(request,"belt/item_page.html", context)

def logout(request):
    if 'id' not in request.session:
        return redirect('/')

    request.session.clear()
    return redirect('/')

## -------- ACTIONS TO ITEMS
def add_item(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        
        name = request.POST['name']
        user = User.objects.get(id=request.session['id'])
        Item.objects.create(name=name, user= user)
        item_id = Item.objects.last()
        # user.wanted_by.create(self)
        return redirect('dashboard')
        # item_id= Item.objects.last().id, user_id=user

def destroy(request, id):
    Item.objects.get(name= request.POST['name']).delete()
    return redirect('dashboard')

def remove(request, id):
    Item.objects.wishlist.get(name= request.POST['name']).delete()
    return redirect('dashboard')

        