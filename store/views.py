from django.shortcuts import render
from .models import storeCategory, storeItem, cartEntry
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
import re


def get_main_page(request, category):
    cat = storeCategory.objects.get(name=category)
    categories = storeCategory.objects.all()
    items = storeItem.objects.filter(category_id=cat.id)
    return render(request, 'store/main_page.html', {'items' : items, 'categories':categories})
    

def get_home_page(request):
    categories = storeCategory.objects.all()
    items = storeItem.objects.all()
    return render(request, 'store/main_page.html', {'items' : items, 'categories':categories})


def get_item_page(request, id):
    user = request.user
    categories = storeCategory.objects.all()
    item = storeItem.objects.get(id=id)
    return render(request, 'store/item_page.html', {'item' : item, 'categories':categories })

def get_user_page(request):
    if request.user.is_authenticated:
        cart_items = cartEntry.objects.filter(user_id=request.user.id)
        total = 0
        for item in cart_items:
            total += item.item_id.price * item.quantity
        return render(request, 'store/user_page.html', {'cart_items':cart_items, 'total':total })
    else:
        return HttpResponseRedirect('/login')

def login_user(request):
    contents = request.POST
    user = authenticate(username=contents.get('username'), password=contents.get('password'))
    request.user = user
    return HttpResponseRedirect('/accounts/profile')



def update_user(request):
    contents = request.POST
    user = request.user
    if user.check_password(contents.get('password')):
        print(user)
        if len(contents.get('new_password')) >= 8:
             user.set_password(contents.get('new_password'))
        if re.match(r'.+@\w+.com', contents.get('email')):
            user.email = contents.get('email')
        if len(contents.get('first_name')) > 1:
            user.first_name = contents.get('first_name')
            print(10)
        if len(contents.get('last_name')) > 1:
            user.last_name = contents.get('last_name')
        user.save()
    return HttpResponseRedirect('/accounts/profile')

def get_signup_page(request):
    return render(request, 'registration/signup.html', {})

def create_user(request):
    contents = request.POST
    if contents.get('password') == contents.get('new_password'):
        user = User.objects.create_user(contents.get('username'), contents.get('email'), contents.get('password'))
        if len(contents.get('first_name')) >= 2:
            user.first_name = contents.get('first_name')
        if len(contents.get('last_name')) >= 2:
            user.last_name = contents.get('last_name')
        user.save()
    return HttpResponseRedirect('/accounts/profile')


def add_to_cart(request):
    item = storeItem.objects.get(id=request.POST.get('item_id'))
    try:
        entry = cartEntry.objects.get(user_id=request.user, item_id=item)
        entry.quantity += 1
    except:
        entry = cartEntry(user_id=request.user, item_id=item)
    entry.save()
    return HttpResponseRedirect('/items/'+str(item.id))

def update_cart(request, id):
    entry = cartEntry.objects.get(id=request.POST.get('id'))
    new_quantity = request.POST.get('quantity')
    if int(new_quantity) == 0:
        entry.delete()
    else:
        entry.quantity = new_quantity
        entry.save()
    return HttpResponseRedirect('/accounts/profile')