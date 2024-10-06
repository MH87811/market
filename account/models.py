from unittest import TestResult

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db.models.signals import post_save
from django.utils import timezone
from django.forms import ModelForm
from django.db.models.signals import post_save
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password, is_shop):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            is_shop=is_shop,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
            is_shop=True
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        blank=True
    )
    # class Meta:
    #     model = Profile
    #     fields = ['user', 'first_name', 'last_name', 'photo']



    username = models.CharField(unique=True, max_length=255, blank=True)
    is_active = models.BooleanField(default=True, blank=True)
    is_admin = models.BooleanField(default=False, blank=True)
    is_shop = models.BooleanField(default=False, blank=True)
    verified = models.BooleanField(default=False, blank=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



class Profile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name="Profile", blank=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    photo = models.ImageField(upload_to='Profile_image/', default='Profile_image/default.png')
    bio = models.CharField(max_length=500, blank=True)
    shop = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=200, blank=True)

    def average_rating(self):
        ratings = Rating.objects.filter(user=self)
        if ratings.exists():
            return sum(rating.value for rating in ratings) / ratings.count()
        return 0

class Rating(models.Model):
    user = models.ForeignKey(Profile, related_name='ratings', on_delete=models.CASCADE)
    rator = models.ForeignKey(MyUser, related_name='ratings', on_delete=models.CASCADE)
    rate = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    # def __str__(self):
    #     return f"{self.user} rated {self.item} with {self.value} stars"