from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, CartItem

class SignupForm(UserCreationForm):   
    class Meta:
        model = User 
        fields = ['username','email','phone_number','password1','password2']
    
class UpdateItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']
