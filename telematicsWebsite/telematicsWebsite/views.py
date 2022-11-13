from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.views import generic
from django.urls import reverse_lazy
from .forms import edit_profile_form
from django.contrib.auth.decorators import login_required

def send_to_home(request):
   return render(request, 'index.html')

@login_required
def index(request):
    return send_to_home(request)

@login_required
def home(request):
    return send_to_home(request)

@login_required
def fleet(request):
    return render(request, 'fleet.html')

@login_required    
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = edit_profile_form(request.POST)
        if form.is_valid():
            if user.is_authenticated:
                try:
                    user.first_name = form.cleaned_data['firstname']
                    user.last_name = form.cleaned_data['lastname']
                    user.email = form.cleaned_data['email']
                    user.username = form.cleaned_data['username']
                    user.account.phone = form.data['phone']
                    user.save()
                    user.account.save()
                    print('User saved')
                except Exception as e:
                    return HttpResponse(e)
            return send_to_home(request)
    return render(request, 'edit_profile.html' )