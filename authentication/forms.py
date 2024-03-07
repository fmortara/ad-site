from django.forms import ModelForm
# importing default user registration form
from django.contrib.auth.forms import UserCreationForm
# importing built-in user model
from django.contrib.auth.forms import User
from django import forms
from ads.models import Author

from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

class UserRegistrationForm(UserCreationForm):
    # Styling the username form fields
    username = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',  
        'name': 'username', 
        'placeholder': 'Nome para usuário'
    }))

    # Styling the password1 form fields
    password1 = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'password',
        'class': 'form-control',  
        'name': 'password1', 
        'placeholder': 'Senha'
    }))

    # Styling the password2 form fields
    password2 = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'password',
        'class': 'form-control',  
        'name': 'password2', 
        'placeholder': 'Repetir a senha'
    }))
    
    # Making the email field required 
    email = forms.EmailField(required=True)

    # Styling the email form fields
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'type': 'email',
        'class': 'form-control',  
        'placeholder': 'Enderço de Email'
    }))

    
    
    class Meta:
        model = User
        fields = ['username','email','password1','password2']


    def clean_email(self):
        email = self.cleaned_data['email']
        duplicate_email = User.objects.filter(email=email).exists()
        # print("Email Taken")
        if duplicate_email:
            raise forms.ValidationError("Esse endereço de email já está cadastrado.")
        return email


class EmailValidationOnForgotPassword(PasswordResetForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={
        'type': 'email',
        'class': 'form-control',  
        'placeholder': 'Endereço de Email'
    }))

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError("Não encontramos registros com esse email no cadastro!")

        return email

class EmailSetPassword(SetPasswordForm):
    # Styling the password1 form fields
    new_password1 = forms.CharField(label="", widget=forms.TextInput(attrs={
        'type': 'password',
        'class': 'form-control',  
        'name': 'new_password1', 
        'placeholder': 'Senha'
    }))

    # Styling the password2 form fields
    new_password2 = forms.CharField(label="", widget=forms.TextInput(attrs={
        'type': 'password',
        'class': 'form-control',  
        'name': 'new_password2', 
        'placeholder': 'Repetir senha'
    }))

# Updating the User registration form
class UserUpdateForm(ModelForm):
    first_name = forms.CharField(label="Nome", widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',  
        'name': 'first_name', 
        'placeholder': 'Nome'
    }))

    last_name = forms.CharField(label="Sobrenome", widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control',  
        'name': 'last_name', 
        'placeholder': 'Sobrenome'
    }))

    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={
        'type': 'email',
        'class': 'form-control',  
        'placeholder': 'Endereço de Email'
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        # exclude = ['user']

# Updating the profile form
class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Author
        fields = ['profile_pic']