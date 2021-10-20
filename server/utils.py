from django.views import View
from django.shortcuts import render, redirect
from django import forms

class MyView(View):
    context = {}
    def render(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)
    def has_permission(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return True
        elif self.permission <= 9999 and request.user.is_authenticated:
            return True
        else:
            return False
    
def has_perm(func):
    def inner(self, request, *args, **kwargs):
        if not self.has_permission(request, *args, **kwargs):
            return redirect('login-page')
        return func(self, request, *args, **kwargs)
    return inner

############# forms #######################
class DateInput(forms.DateInput):
    input_type = 'date'
class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime'
class PasswordInput(forms.PasswordInput):
    input_type = 'password'
    
class MyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'