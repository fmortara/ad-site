from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import *
from django.core.exceptions import ValidationError

class AskForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',  
        'name': 'name', 
        'placeholder': 'Seu nome'
    }))

    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'form-control',  
        'name': 'email', 
        'placeholder': 'Email para contato'
    }))

    message = forms.CharField(widget=CKEditorWidget(attrs={
        'type': 'text',
        'class': 'form-control',  
        'name': 'message', 
        'placeholder': 'Mensagem para o anunciante'
    }))


    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',  
        'name': 'phone', 
        'placeholder': 'Telefone para contato'
    }))

    def clean_message(self):
        data = self.cleaned_data['message']

        # Check if the message does not contain phone number or emails
        # TO DO

        return data

class RespostaForm(forms.Form):
    message = forms.CharField(widget=CKEditorWidget(attrs={
        'type': 'text',
        'class': 'form-control',
        'name': 'message',
        'label': 'Resposta',
        'placeholder': 'Resposta da pergunta feita pelo interessado'
    }))

    
        