from _lsprof import profiler_subentry
from lib2to3.pygram import pattern_symbols

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseNotFound
from pyexpat.errors import messages
from django.db.models import Count, Q, F
from shopcart.models import *
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from kavenegar import *
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
import random


# Create your views here.

def Login(request):
    if request.method == 'POST':
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:index')
        else:
            return HttpResponse('false')
    else:
        return render(request, 'LoginRegister.html')

def EmailLoginToken(request):
    if request.method == 'POST':
        if MyUser.objects.filter(email=request.POST['email']).exists():
            request.session['login_token'] = random.randint(100000, 999999)
            token = request.session['login_token']
            subject = 'Login To Market'
            message = render_to_string('verification_email.html', {'token': token})
            request.session['email'] = request.POST['email']
            email = request.POST['email']
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return redirect('account:email_login')
        else:
            return HttpResponse('User with this email is not registered on this site')
    else:
        return render(request, 'EmailLogin.html')


def EmailLoginVerify(request):
    if request.method == 'POST':
        if 'token' in request.POST:
            try:
                submitted_token = int(request.POST['token'])
            except ValueError:
                return HttpResponse('Invalid token format', status=400)

            if submitted_token == request.session.get('login_token'):
                email = request.session.get('email')
                try:
                    target = MyUser.objects.get(email=email)
                    print('username is', target.username, 'and password is', target.password, 'email is', email)
                except MyUser.DoesNotExist:
                    return HttpResponse('User Not Found', status=404)

                user = authenticate(request, email=email, token=request.session.get('token'))
                print(user)
                if user is not None:
                    login(request, user)
                    return redirect('main:index')
                else:
                    return HttpResponse('Authentication failed', status=401)
            else:
                return HttpResponse('Invalid token', status=403)
        else:
            return HttpResponse('Token not provided', status=400)
    else:
        return render(request, 'login_verify.html')


def Register(request):
    if request.user.is_authenticated:
        return HttpResponse('login')
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        conf = 1
        username = form['username'].value()
        email = form['email'].value()
        is_shop = form['is_shop'].value()
        if request.POST['password'] != request.POST['password2']:
            return HttpResponse('incorrect password')
            conf = 0
        if form.is_valid() and conf == 1:
            data = form.cleaned_data
            myuser = MyUser.objects.create_user(email=data['email'], username=data['username'], password=data['password'], is_shop=data['is_shop'])
            myuser.save()
            user = authenticate(request, email=data['email'], password=data['password'])
            login(request, user)
            Profile.objects.create(user=request.user, first_name='', last_name='', phone='', bio='', shop='')
            return redirect('account:EditProfile')
        else:
            return HttpResponse('not')
    else:
        form = UserCreateForm()
    context = {'form': form}
    return render(request, 'LoginRegister.html', context)


@login_required(login_url='account:Login')
def Logout_view(request):
    logout(request)
    return redirect('main:index')


@login_required(login_url='account')
def ProfileUpdate(request):
    user = MyUser.objects.get(id=request.user.id)
    user_info = [user.username, user.email]
    profile = Profile.objects.get(user_id=request.user.id)
    profile_info = [profile.first_name, profile.last_name, profile.phone, profile.photo, profile.bio, profile.address, profile.shop]
    if request.method == 'POST':
        if request.user.is_shop:
            user_form = UserUpdateForm(request.POST, instance=user, use_required_attribute=False)
            profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile, use_required_attribute=False)
        else:
            user_form = ShopUpdateForm(request.POST, instance=user, use_required_attribute=False)
            profile_form = ProfileUpgradeForm(request.POST, request.FILES, instance=profile, use_required_attribute=False)

        if user_form.is_valid() and profile_form.is_valid():
            user_data = user_form.cleaned_data
            profile_data = profile_form.cleaned_data
            user.username = user_info[0] if user_data['username'] is '' else user_data['username']
            user.email = user_info[1] if user_data['email'] is '' else user_data['email']
            if request.user.is_shop == False:
                user.is_shop = user_data.get('is_shop', False)
            user.save()

            if request.user.is_shop:
                profile.shop = profile_info[6] if profile_data['shop'] is '' else profile_data['shop']
            profile.first_name = profile_info[0] if profile_data['first_name'] is None else profile_data['first_name'] #done
            profile.last_name = profile_info[1] if profile_data['last_name'] is None else profile_data['last_name'] #done
            profile.phone = profile_info[2] if profile_data['phone'] is None else profile_data['phone'] #done
            profile.photo = profile_info[3] if profile_data['photo'] is '' else profile_data['photo']
            profile.bio = profile_info[4] if profile_data['bio'] is '' else profile_data['bio']
            profile.address = profile_info[5] if profile_data['address'] is '' else profile_data['address']
            profile.save()
            return redirect('account:Profile', id=request.user.id)
        else:
            errors = user_form.errors.as_json() + profile_form.errors.as_json()
            return HttpResponse(f'Your information is invalid: {errors}', status=400)
    else:
        if request.user.is_shop:
            user_form = UserUpdateForm(instance=user, use_required_attribute=False)
            profile_form = ProfileUpdateForm(instance=profile, use_required_attribute=False)
        else:
            user_form = ShopUpdateForm(instance=user, use_required_attribute=False)
            profile_form = ProfileUpgradeForm(instance=profile, use_required_attribute=False)

    context = {'profile_form': profile_form, 'user_form': user_form}
    return render(request, 'UpdateProfile.html', context)



@login_required(login_url='account:Login')
def profile(request, id):
        profiles = Profile.objects.filter(user_id=id)
        products = Product.objects.filter(user_id=id)
        collections = Collection.objects.filter(user_id=id)
        context = {
            'profiles': profiles,
            'products': products,
            'collections': collections,
        }
        return render(request, 'Profile.html', context)

@login_required(login_url='account:Login')
def DisplayProfile(request, id):
    request_profile = Profile.objects.get(user_id=id)
    request_product = Product.objects.filter(user_id=id)
    context = {
        'profile': request_profile,
        'products': request_product,
    }
    return render(request, 'DisplayProfile.html', context)

@login_required(login_url='account:Login')
def DisplayFave(request):
    object = UserFave.objects.filter(user_id=request.user.id)
    context = {
        'fave': object
    }
    return render(request, 'favorite.html', context)

@login_required(login_url='account:Login')
def BuyRequests(request):
    if request.user.is_shop:
        carts = Cart.objects.filter(seller_id=request.user.id, payed=True)
        grouped_orders = carts.values('user_id').annotate(order_count=Count('id'))
        orders_by_user = {}
        for group in grouped_orders:
            user_id = group['user_id']
            orders_by_user[user_id] = carts.filter(user_id=user_id)
        if grouped_orders:
            first_user_id = grouped_orders[0]['user_id']
            customer = Profile.objects.get(user_id=first_user_id)
        else:
            customer = None
        context = {
            'carts': carts,
            'orders_by_user': orders_by_user,
            'customer': customer,
        }
        return render(request, 'requests.html', context)
    else:
        raise PermissionDenied()


@login_required(login_url='account:Login')
def AcceptRequest(request, cart_id, user_id):
    if request.user.is_shop:
        if Cart.objects.filter(id=cart_id, user_id=user_id).exists():
            cart = Cart.objects.filter(seller_id=request.user.id, user_id=user_id)
            for i in cart:
                SellHistory.objects.create(
                    buyer_id=i.user.id,
                    buyer_profile_id=i.buyer_profile.id,
                    product_id=i.product.id,
                    quantity=i.quantity,
                    seller_id=i.seller_id,
                )
                cart.delete()
            return redirect('account:requests')
        else:
            return HttpResponseNotFound()
    else:
        raise PermissionDenied
@login_required(login_url='account:Login')
def ChangePassword(request):
    if request.method == 'POST':
        form = SeetPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('account:Profile', id=request.id)
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = SeetPasswordForm(request.user)
        return render(request, 'ChangePassword.html', {'form': form})

@login_required(login_url='/login/')
def delete_user(request, email):
    if request.method == 'POST':
        try:
            user = MyUser.objects.get(email=email)
            profile = Profile.objects.get(user_id=user.id)
            user.delete()
            profile.delete()
        except Exception as e:
            print(e)
    else:
        return render(request, 'forgot.html')
    return render(request, 'forgot.html')

@login_required(login_url='account:Login')
def Send_Verify_Code(request):
    request.session['token'] = random.randint(100000, 999999)
    token = request.session['token']
    subject = 'Verify Your Email Address'
    message = render_to_string('verification_email.html', {'token': token})
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [request.user.email],
        fail_silently=False,
    )
    return redirect('account:verify')

@login_required(login_url='account:Login')
def Verify(request):
    if request.method == 'POST':
        submitted_token = int(request.POST['token'])
        if submitted_token == request.session.get('token'):
            user = MyUser.objects.get(id=request.user.id)
            user.verified = 1
            user.save()
            return HttpResponse('good')
        else:
            return HttpResponse('fuck')
    else:
        return render(request, 'verify.html')