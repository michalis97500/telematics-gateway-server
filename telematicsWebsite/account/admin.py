from account.models import Account
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class AccoutInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = 'Accounts'

class CustomUserAdmin(UserAdmin):
  inlines = (AccoutInline, )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Account)