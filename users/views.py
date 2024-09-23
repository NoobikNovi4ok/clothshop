from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import render
from users.forms import UserLoginForm, UserRegistrationForm
from django.contrib import auth
from django.urls import reverse
from django.contrib import messages
from users.models import User


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            login = request.POST["login"]
            password = request.POST["password"]
            user = auth.authenticate(login=login, password=password)
            if user:
                auth.login(request, user)
                messages.add_message(
                    request, messages.INFO, f"{user} вы успешно вошли в аккаунт"
                )
                return HttpResponseRedirect(reverse("home"))
        else:
            messages.error(
                request,
                "Неправильный логин или пароль. Попробуйте еще раз",
                extra_tags="password_login",
            )
    else:
        form = UserLoginForm()

    context = {
        "title": "Авторизация",
        "form": form,
    }

    return render(request, "users/login.html", context)


def registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if (
            form.is_valid()
            and (form.data["password"] == form.data["password_repeat"])
            and not (
                form.data["email"] in User.objects.all().values_list("email", flat=True)
            )
        ):
            form.save()
            messages.add_message(
                request,
                messages.INFO,
                f'{form.data["name"]} вы успешно создали в аккаунт',
            )
            return HttpResponseRedirect(reverse("user:login"))
        else:
            if form.data["login"] in User.objects.all().values_list("login", flat=True):
                messages.error(
                    request, "Логин занят. Введите другой", extra_tags="name"
                )
            elif form.data["email"] in User.objects.all().values_list(
                "email", flat=True
            ):
                messages.error(
                    request, "Почта занята. Введите другую", extra_tags="email"
                )
            elif form.errors.as_data() == {"password_repeat"}:
                messages.error(
                    request,
                    "Пароль короче 8 символов или содержит только цифры",
                    extra_tags="password",
                )
            elif form.data["password"] != form.data["password_repeat"]:
                messages.error(request, "Пароли не совпадают", extra_tags="passwords")
    else:
        form = UserRegistrationForm()

    context = {
        "title": "Регистрация",
        "form": form,
    }

    return render(request, "users/registration.html", context)
