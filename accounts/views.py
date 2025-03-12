from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])  # Хешируем пароль
            user.save()
            login(request, user)  # Автоматически логиним пользователя
            return redirect("dashboard")  # После регистрации перенаправляем на главную
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")  # После входа перенаправляем на главную
        else:
            return render(request, "accounts/login.html", {"error": "Неверный логин или пароль"})

    return render(request, "accounts/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")  # После выхода перенаправляем на страницу входа

@login_required
def dashboard(request):
    return render(request, "accounts/dashboard.html")
