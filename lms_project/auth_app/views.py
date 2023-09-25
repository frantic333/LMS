from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import User


def log_in(request):
    if request.method == 'POST':
        data = request.POST
        user = authenticate(email=data['email'], password=data['password'])
        if user and user.is_active:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse('Ваш аккаунт заблокирован')
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        data = request.POST
        user = User(email=data['email'], first_name=data['first_name'], last_name=data['last_name'],
                    birthday=data['birthday'], description=data['description'], avatar=data['avatar'])
        user.set_password(data['password'])
        user.save()
        login(request, user)
        return redirect('index')
    else:
        return render(request, 'register.html')



def logout(request):
    logout(request)
    return redirect('log_in')


def change_password(request):
    return HttpResponse('Этот обработчик меняет пароль пользователя')


def reset_password(request):
    return HttpResponse('В этом обработчике реализована логика сброса пароля пользователя')