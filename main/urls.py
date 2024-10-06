from django.urls import path
from .views import *
from shop.views import *

app_name = 'main'

urlpatterns = [
    path('home/', index, name='index'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('detail/', detail, name='detail'),
    path('faq/', FAQ, name='faq'),
    path('feature/', feature, name='feature'),
    path('gallery/', DisplayMultiple, name='gallery'),
    path('pricing/', pricing, name='pricing'),
    path('sellers/', sellers, name='sellers')
]