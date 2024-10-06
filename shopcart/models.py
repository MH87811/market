from django.db import models
from account.models import *
from shop.models import *
from django.forms import ModelForm

# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='buyer', related_name='buyer')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='selling')
    buyer_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="تعداد")
    seller = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='seller')
    payed = models.BooleanField(default=False)
    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبد خرید"


class SellHistory(models.Model):
    seller = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='Sell_History_Seller')
    buyer = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='Sell_History_Buyer')
    buyer_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='Sell_History_Buyer_Profile')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='Sell_History_Product')
    quantity = models.PositiveIntegerField()