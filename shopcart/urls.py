from django.urls import path
from .views import *

app_name='cart'

urlpatterns = [
    path('cart/', cart, name='cart'),
    path('add_to_cart/<int:id>,<int:seller_id>/', add_to_cart, name='add_to_cart'),
    path('remove_cart/<int:id>/', remove_cart, name='remove_cart'),
    path('add_single/', UpdateCart, name='add_single'),
    path('continueshopping/', ContinueShopping, name='Continue')
    # path('remove_single/<int:id>/', remove_single, name='remove_single'),
]