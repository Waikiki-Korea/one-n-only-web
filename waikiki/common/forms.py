from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ono.models import OnoUser

class UserForm(UserCreationForm):
    email = forms.EmailField(label="email")

    class Meta:
        model = OnoUser
        fields = ("username", "password1", "password2", "email", "eth_address")
