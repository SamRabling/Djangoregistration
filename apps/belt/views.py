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
    return render(request,"belt/index.html")

def dashboard(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id = request.session['id'])
        mylist = user.wished.all()
        items = Item.objects.all()
        others = Item.objects.exclude(owner_id = request.session['id'])
        context = {
            'user':user,
            'mylist': mylist,
            'items': items,
            'others': others
	    }
        print "dashboard engaged"
        return render(request,"belt/dashboard.html", context)

def add(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['id'])
        context={
            'user': user,
        }
        return render(request, 'belt/add.html', context)

def add_to_wishlist(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        errors = Item.objects.item_basic_validator(request.POST)  
        if len(errors):
            for tag, errors in errors.iteritems():
                messages.error(request, errors,  extra_tags=tag)
                return redirect('add')
        user = User.objects.get(id = request.session['id'])
        print "user saved"
        Item.objects.create(name=request.POST['name'], owner= user)
        item = Item.objects.last()
        print "wish saved"
        item.wishlist.add(user)
        # wish.save()
        print "wish added"
        return redirect('../dashboard')

def item(request, id):
    if 'id' not in request.session:
        return redirect('/')
    else:
        item = Item.objects.get(id=id)
        context={
            'item': item,
            'wishers': item.wishlist.all()
        }

    return render(request,"belt/item_page.html", context)

def add_to_my_wishlist(request, id):
    wisher = User.objects.get(id = request.session['id'])
    print "wisher saved"
    item = Item.objects.get(id=id)
    print "item saved"

    item.wishlist.add(wisher)
    item.save()
    print "wish added"
    return redirect('/dashboard')

def un_wish(request, id):
    item = Item.objects.get(id=id)
    item.save()
    wisher = User.objects.get(id = request.session['id'])
    wisher.save()
    item.wishlist.remove(wisher)
    return redirect('../../dashboard')

def destroy(request, id):
    Item.objects.get(name= request.POST['name']).delete()
    return redirect('dashboard')

def logout(request):
    if 'id' not in request.session:
        return redirect('/')

    request.session.clear()
    return redirect('/')

# ## -------- ACTIONS TO ITEMS
# def edit_wishlist(request, operation, pk):
#     if 'id' not in request.session:
#         return redirect('/')
#     else:
#         user = User.objects.get(id=request.session['id'])
#         if Item.objects.filter(name=postData['name']) == []:
#             new_item = Item.objects.get(pk=pk)
#             if operation == 'add':
#                 Wishlist.wished_item(user, new_item)
#             elif operation == 'remove':
#                 Wishlist.remove_item(user,new_item)
#         else:
#             name = request.POST['name']
#             Item.objects.create(name=name, user=user)
#             Wishlist.wished_item(user, new_item)
#         return redirect('dashboard')
#         # item_id= Item.objects.last().id, user_id=user




        