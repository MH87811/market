from django.urls import path
from .views import *

app_name = 'shop'

urlpatterns = [
    path('AddProduct/', AddProduct, name='AddProduct'),
    path('single/<int:id>', DisplaySingle, name='single'),
    path('multiple/', DisplayMultiple, name='Multiple'),
    path('personal/<int:id>', DisplayPersonal, name='Personal'),
    path('product_like/<int:id>', ProductLikes, name='like'),
    path('product_fave/<int:id>', ProductFave, name='fave'),
    path('add_category/', AddCategory, name='AddCategory'),
    path('addcomment/<int:id>', AddComment, name='AddComment'),
    path('createcollection/', CreateCollection, name='CreateCollection'),
    path('categoryproducts/<int:id>', CategoryProducts, name='cp'),
]