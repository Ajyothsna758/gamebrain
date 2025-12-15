from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

class SignUpForm(UserCreationForm):
    email= forms.EmailField(required=True)
    class Meta:
        model=User
        fields=["username", "email", "password1", "password2"]

class LoginForm(AuthenticationForm):
    username= forms.CharField()        
    password= forms.CharField(widget=forms.PasswordInput)
    error_messages={
        "invalid_login":"Invalid Username or Password"
    }