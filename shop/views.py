from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from pyexpat.errors import messages
from django.views.generic.edit import UpdateView
from django.core.exceptions import PermissionDenied
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages

# Create your views here.
@login_required(login_url='account:Login')
def AddProduct(request):
    if request.user.is_shop:
        if request.method == 'POST':
            form = AddProductForm(request.POST or None, request.FILES, instance=request.user)
            if form.is_valid():
                data = form.cleaned_data
                product = Product.objects.create(
                    user=request.user,
                    title=data['title'],
                    description=data['description'],
                    picture=data['picture'],
                    price=data['price'],
                    quantity=data['quantity'],
                )
                if 'category' in request.POST:
                    product.category.set(data['category'])
                else:
                    product.category.set(None)
                return redirect('main:index')
            else:
                return HttpResponse('Invalid form submission')
        else:
            form = AddProductForm()
            return render(request, 'AddProduct.html', {'form': form, 'category': Categories.objects.all()})
    else:
        return HttpResponse('you need to upgrade ro seller')

def DisplayMultiple(request):
    return render(request, 'gallery.html', {'products':Product.objects.all()})
def DisplaySingle(request, id):
    products = Product.objects.filter(id=id)
    product = get_object_or_404(Product, id=id)
    likes = product.likes.count()
    categories = product.category.all()
    comments = Comment.objects.filter(product_id=id)
    others = Product.objects.filter(user_id=product.user.id).exclude(id=id)[0:4]

    context = {
        'products': products,
        'likes': likes,
        'categories': categories,
        'comments': comments,
        'count': comments.count(),
        'others': others,
    }
    return render(request, 'SingleProduct.html', context)
@login_required(login_url='account:Login')
def DisplayPersonal(request, id):
    product = Product.objects.filter(user_id=id)
    context = {
        'products': product,
    }
    return render(request, 'Personal_gallery.html', context)
@login_required(login_url='account:Login')
def ProductLikes(request, id):
    post = get_object_or_404(Product, id=request.POST.get('product_slug'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('shop:single', id=id)

@login_required(login_url='account:Login')
def ProductFave(request, id):
    if UserFave.objects.filter(user_id=request.user.id, product_id=id).exists():
        UserFave.objects.filter(user_id=request.user.id, product_id=id).delete()
        return redirect('shop:single', id=id)
    else:
        UserFave.objects.create(user_id=request.user.id, product_id=id)
        return redirect('shop:single', id=id)
@login_required(login_url='account:Login')
def AddCategory(request):
    if request.method == 'POST':
        form = AddCategoryForm(request.POST or None, request.FILES)
        if form.is_valid():
            Categories.objects.create(
                user=request.user,
                title=form.cleaned_data['title'],
                image=form.cleaned_data['image'],
            )
            return redirect('main:index')
        else:
            return HttpResponse('invalid data')
    else:
        form=AddCategoryForm()
        return render(request, 'AddCategory.html', {'form':form})

@login_required(login_url='account:Login')
def CategoryProducts(request, id):
    products = Product.objects.filter(category=id)
    context = {
        'products': products,
    }
    return render(request, 'CategoryProducts.html', context)

@login_required(login_url='account:Login')
def AddComment(request, id):
    if request.method == 'POST':
        form = AddCommentForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            product = Product.objects.get(id=id)
            Comment.objects.create(
                user=request.user,
                product=product,
                msg=data['msg'],
            )
        return redirect('shop:single', id=id)
    else:
        return HttpResponse('method invalid')

@login_required(login_url='account:Login')
def CreateCollection(request):
    if request.user.is_shop:
        if request.method == 'POST':
            form = CreateCollectionForm(request.POST or None, request.FILES)
            if form.is_valid():
                data = form.cleaned_data
                Collection.objects.create(user_id=request.user.id, name=data['name'], products_id=None, image=data['image'])
                return redirect('account:Profile', id=request.user.id)
        else:
            form = CreateCollectionForm
            return render(request, 'CreateCollection.html', {'form': form})
    else:
        raise PermissionDenied
