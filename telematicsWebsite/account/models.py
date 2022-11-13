from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Account(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  phone = PhoneNumberField(null=False, blank=False, unique=True)
  
  def __str__(self):
    return self.user.username
  
  def get_phone(self):
    return self.user.account.phone.as_e164