from django.contrib import admin
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from account.forms import UserForm

from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth import authenticate


def signup(request):
    form = UserForm()
    if request.method == "POST":
        form = UserForm(request.POST)
            
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            message = 'este nombre de usuario ha sido registrado'
            return render(request, 'registration/signup.html', {"message": message, "form":form})
        user = User()
        user.username = username
        user.set_password(password)
        user.save()
        return render(request,'registration/login.html',{"form":form})
    else:
        return render(request, 'registration/signup.html',{"form":form})


def profile(request):
    return render(request,'registration/profile.html')
