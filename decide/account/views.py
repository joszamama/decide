from django.contrib import admin
from django.contrib.auth import login, authenticate
from django.contrib.auth.signals import user_logged_in
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from account.forms import UserForm

from django.db import models
from django.contrib.auth.models import User
from census.models import Census

def signup(request):
    form = UserForm()
    if request.method == "POST":
        form = UserForm(request.POST)
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            message = 'Este usuario ya ha sido registrado'
            return render(request, 'registration/signup.html', {"message": message, "form":form})
        user = User()
        user.username = username
        user.email = email
        user.set_password(password)
        user.save()
        if User.objects.filter(username=username).exists():
            message = 'Se ha registrado correctamente. Puede Iniciar Sesión'
            return render(request, 'registration/signup.html', {"message": message, "form":form})
    else:
        return render(request, 'registration/signup.html',{"form":form})

def view_login(request):
    form = UserForm()
    if request.method == "POST":
        form = UserForm(request.POST)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password) 
        if user is not None:
            login(request,user)
            return HttpResponseRedirect('/account/profile')
        else:
            message = 'Usuario o contraseña incorrecta'
            return render(request, 'registration/login.html', {'form': form, 'message':message})
    else:
        return render(request,'registration/login.html',{'form':form})


def profile(request):
    user = request.user
    votaciones = Census.objects.filter(voter_id=user.id).values_list('voting_id')
    votacio = votaciones.all()
    v = list(votacio[0])
    return render(request,'registration/profile.html',{'id_votacion':str(v[0])})

def updateUser(request):
    user = request.user
    form = UserForm(instance = user)
    if request.method == "POST":
        emailActual = user.email
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(email=email).exists() and email!=emailActual:
            message = 'Este correo ya existe en la BD'
            return render(request, 'registration/update.html', {"message": message, "form":form})
        
        user.email = email
        user.set_password(password)
        user.save()
        login(request,user, backend='django.contrib.auth.backends.ModelBackend')
        return render(request,'registration/profile.html',{"form":form})
        

    else:
        return render(request, 'registration/update.html',{"form":form})
