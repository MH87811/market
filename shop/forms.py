from django import forms
from .models import *

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'picture', 'price', 'quantity', 'category']

class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ['title', 'image']

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['msg']

class CreateCollectionForm(forms.ModelForm):
        class Meta:
            model = Collection
            fields = ['name', 'image']