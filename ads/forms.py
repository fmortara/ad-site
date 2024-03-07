from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import *

class PostAdsForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',  
        'name': 'title', 
        'placeholder': 'Título'
    }))

    description = forms.CharField(widget=CKEditorWidget(attrs={
        'type': 'text',
        'class': 'form-control',  
        'name': 'description', 
        'placeholder': 'Descrição'
    }))

    price = forms.CharField(widget=forms.NumberInput(attrs={
        'class': 'form-control',  
        'name': 'price', 
        'placeholder': 'Preço'
    }))

    city = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',  
        'name': 'city', 
        'placeholder': 'Cidade'
    }))

    brand = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',  
        'name': 'brand', 
        'placeholder': 'Marca'
    }))

    phone = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',  
        'name': 'phone', 
        'placeholder': 'Telefone'
    }))

    class Meta:
        model = Ads
        fields = '__all__'
        exclude = ['author', 'date_created', 'is_featured']

    

    
        