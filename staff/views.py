from staff.decorators import unauthenticated_user
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from . import forms
from django.contrib import messages
# Create your views here.

@unauthenticated_user
def register(request):
    form = forms.CreateUserForm()
    if request.method == "POST":
        form = forms.CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,"Account was created for " + username)
            return redirect('staff:login')
    
    return render(request,'templates/register.html',{'form':form})

@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username= username, password = password)
        if user is not None:
            login(request, user)
            print(user, "is loged in" )
            return redirect('store:index')
        else:
            messages.error(request,"Username and password does not match")
    
    return render(request, 'templates/login.html')

def logoutUser(request):
    logout(request)
    return render(request, 'templates/login.html')