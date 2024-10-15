from django.shortcuts import render
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages


def registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.add_message(
                request,
                messages.INFO,
                f"{user.name} вы успешно создали в аккаунт",
            )
            return HttpResponseRedirect(reverse("user:login"))

        return render(
            request, "users/registration.html", {"form": form, "title": "Регистрация"}
        )

    else:
        form = UserRegistrationForm()

    return render(
        request, "users/registration.html", {"form": form, "title": "Регистрация"}
    )


def login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            login_input = form.cleaned_data["login"]
            password = form.cleaned_data["password"]
            user = auth.authenticate(request, login=login_input, password=password)

            if user:
                auth.login(request, user)
                messages.add_message(
                    request, messages.INFO, f"{user} вы успешно вошли в аккаунт"
                )
                return HttpResponseRedirect(reverse("home"))
            else:
                form.add_error(None, "Неверный логин или пароль.")

        return render(
            request, "users/login.html", {"form": form, "title": "Авторизация"}
        )

    else:
        form = UserLoginForm()

    return render(request, "users/login.html", {"form": form, "title": "Авторизация"})


def users_basket(request):
    return render(request, "users/users_basket.html")
