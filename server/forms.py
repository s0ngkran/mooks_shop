from django import forms
from .models import *
from django.contrib.auth.models import User
from .utils import *

            
class UserForm(MyForm):
    class Meta:
        model = User
        fields = 'username', 'password'
        widgets = {
            'password': PasswordInput(),
        }
        help_texts = {
            'username': None,
        }
    
class ProfileForm(MyForm):
    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ('user',)
    
    