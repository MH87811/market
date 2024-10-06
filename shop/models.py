from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import timezone
from django.forms import ModelForm
from django.db.models.signals import post_save
from django.utils import timezone
from account.models import *

# Create your models here.
class Categories(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_image/')
    position = models.SlugField()
    class Meta:
        ordering = ['position']
    def __str__(self):
        return self.title

class Product(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='Product_User')
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    picture = models.ImageField(null=False, blank=False, upload_to='Product_image/')
    publish = models.DateTimeField(default=timezone.now)
    price = models.IntegerField(null=False, blank=False)
    slug = models.SlugField(blank=True)
    quantity = models.IntegerField(null=False, blank=False)
    likes = models.ManyToManyField(MyUser, related_name='product_likes', blank=True, verbose_name='product_likes')
    category = models.ManyToManyField(Categories, null=True)
    def __str__(self):
        return self.title

class UserFave(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
class Comment(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    msg = models.CharField(max_length=500)
    publish = models.DateTimeField(default=timezone.now)

class Collection(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='collection_user')
    name = models.CharField(max_length=25)
    products = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='collection_products', null=True)
    image = models.ImageField(null=True, blank=True, upload_to='Collection_image/')