from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User
        
        

        

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, required=False)
    email = forms.EmailInput()
    password = forms.CharField(widget=forms.PasswordInput)
    
