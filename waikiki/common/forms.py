from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from ono.models import OnoUser

class UserForm(UserCreationForm):
    # email = forms.EmailField(label="email")
    symbol = forms.ImageField(label="symbol", required=False)
    class Meta:
        model = OnoUser
        fields = ("username", "password1", "password2", "email", "eth_address", "symbol")

class OnoUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ("email", "eth_address")