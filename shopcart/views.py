from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from shop.models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.

@login_required(login_url='account:Login')
def cart(request):
    card = Cart.objects.filter(user_id=request.user.id)
    user = request.user
    total = 0
    for cards in card:
        total += cards.quantity * cards.product.price
    context = {
        'card': card,
        'total': total,
        'user': user
    }
    return render(request, 'cart.html', context)


@login_required(login_url='account:Login')
def add_to_cart(request, id, seller_id):
    quantity = 1
    profile = Profile.objects.get(user_id=request.user.id).id
    product = get_object_or_404(Product, id=id)
    if quantity <= product.quantity:
        if Cart.objects.filter(user_id=request.user.id, product_id=id).exists():
            card = Cart.objects.get(user_id=request.user.id, product_id=id, seller=seller_id, buyer_profile_id=profile)
            card.quantity += 1
            card.save()
            return redirect('cart:cart')
        else:
            card = Cart.objects.create(quantity=quantity, product_id=id, user_id=request.user.id, seller_id=seller_id, buyer_profile_id=profile)
            card.save()
            return redirect('cart:cart')
    else:
        return HttpResponse('Too Much')


@login_required(login_url='account:Login')
def remove_cart(request, id):
    card = Cart.objects.get(id=id)
    card.delete()
    return redirect('cart:cart')

@login_required(login_url='account:Login')
def UpdateCart(request):
    product_id = request.POST['product_id']
    product = Product.objects.get(id=product_id)
    new_quantity = int(request.POST['quantity'])
    if Cart.objects.filter(user_id=request.user.id, product_id=product_id).exists():
        if new_quantity <= product.quantity:
            cart = Cart.objects.get(user_id=request.user.id, product_id=product_id)
            cart.quantity = new_quantity
            cart.save()
            return redirect('cart:cart')
        else:
            return HttpResponse('too much')
    else:
        cart = Cart.objects.create(quantity=1, product_id=product_id, user_id=request.user.id)
        return redirect('cart:cart')

def ContinueShopping(request):
    user = MyUser.objects.get(id=request.user.id)
    if user.verified == True:
        Cart.objects.filter(user_id=request.user.id).update(payed=1)
        return redirect('main:index')
    else:
        return redirect('account:send')