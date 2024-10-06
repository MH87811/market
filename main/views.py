from django.shortcuts import render, redirect
from .forms import *
from shop.models import *
from shopcart.models import *
from django.db.models import Count
from django.db import models

# Create your views here.


def index(request):
    return render(request, 'index.html', {'most_liked_products': Product.objects.annotate(like_count=models.Count('likes')).order_by('-like_count')[0:5]})
def about(request):
    return render(request, 'about.html')
def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['msg']
        Contact.objects.create(name=name, email=email, phone=phone, msg=message)
        return redirect('main:index')
    else:
        return render(request, 'contact.html')
def detail(request):
    return render(request, 'detail.html')
def FAQ(request):
    return render(request, 'faq.html')
def feature(request):
    return render(request, 'feature.html')
def pricing(request):
    products = Product.objects.annotate(like_count=Count('likes')).order_by('-like_count')[0:5]
    context = {
        'products': products
    }
    return render(request, 'pricing.html', context)
def sellers(request):
    return render(request, 'team.html', { 'sellers':Profile.objects.all() })