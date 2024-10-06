from django import forms
from .models import *
from django.contrib.auth.forms import SetPasswordForm


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'is_shop']

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password_Confirmation']:
            raise forms.ValidationError('Passwords are not the same')
        return data['password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password_Confirmation'])
        if commit:
            user.save()
        return user

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone', 'photo', 'bio', 'shop', 'address']

class ProfileUpgradeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone', 'photo', 'bio', 'address']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['email', 'username']
class ShopUpdateForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['email', 'username', 'is_shop']


class SeetPasswordForm(SetPasswordForm):
    class Meta:
        model = MyUser
        fields = ['new_password', 'confirm']

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rate']
        widgets = {
            'rate': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
        }