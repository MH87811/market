from django.contrib import admin
from .models import *
from account.models import *
from shop.models import *

# Register your models here.

admin.site.register(MyUser)
admin.site.register(Product)
admin.site.register(Categories)
