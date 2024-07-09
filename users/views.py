from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm

from users.forms import RegistrationForm


def login_user(request: HttpRequest):
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request,
                username=data["username"],
                password=data["password"],
            )
            if user and user.is_active:
                login(request, user)
                return redirect("index")
    else:
        form = AuthenticationForm()

    context = {
        "title": "Войти",
        "form": form,
    }
    return render(request, "users/login.html", context=context)


def logout_user(request: HttpRequest):
    logout(request)
    return redirect("index")


def register(request: HttpRequest):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return render(request, "users/registration_done.html")
    else:
        form = RegistrationForm()
    return render(request, "users/registration.html", {"form": form})
