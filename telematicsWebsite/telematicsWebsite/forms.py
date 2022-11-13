from django import forms
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator


class edit_profile_form(forms.Form):
  firstname = forms.CharField(label='First name', max_length=100,)
  lastname = forms.CharField(label='Last name', max_length=100)
  email = forms.EmailField(label='Email', max_length=100)
  username = forms.CharField(label='Username', max_length=150)
  phone = PhoneNumberField()
  