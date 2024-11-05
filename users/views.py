from django.shortcuts import render
from django.contrib.auth.views import LoginView
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from orders.models import Order, OrderItem
from django.db.models import Prefetch
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, redirect

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
    # return render(
    #      request, "main/layout.html", {"form": form, "title": "Регистрация"}
    #  )

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('users:profile')
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            login_value = form.cleaned_data.get('login')
            password = form.cleaned_data.get('password')
            user = authenticate(request, login=login_value, password=password)

            if user is not None:
                login(request, user)
                messages.add_message(
                     request, messages.INFO, f"{user} вы успешно вошли в аккаунт"
                )
                return redirect(self.success_url)
            else:
                form.add_error(None, "Неверный логин или пароль.")  # Общая ошибка

        return render(request, self.template_name, {'form': form})

# def login(request):
#     if request.method == "POST":
#         form = UserLoginForm(request.POST)
#         if form.is_valid():
#             login_input = form.cleaned_data["login"]
#             password = form.cleaned_data["password"]
#             user = auth.authenticate(request, login=login_input, password=password)

#             if user:
#                 auth.login(request, user)
#                 messages.add_message(
#                     request, messages.INFO, f"{user} вы успешно вошли в аккаунт"
#                 )
#                 return HttpResponseRedirect(reverse("home"))
#             else:
#                 form.add_error(None, "Неверный логин или пароль.")

#         return render(
#             request, "users/login.html", {"form": form, "title": "Авторизация"}
#         )

#     else:
#         form = UserLoginForm()

#     return render(request, "users/login.html", {"form": form, "title": "Авторизация"})

@login_required
def profile(request):
    orders = (
        Order.objects.filter(user=request.user)
        .prefetch_related(
            Prefetch(
                "orderitem_set",
                queryset=OrderItem.objects.select_related("product"),
            )
        )
        .order_by("-id")
    )

    for order in orders:
        order.total_price = sum(item.products_price() for item in order.orderitem_set.all())

    context = {"title": "Профиль пользователя",  "orders": orders }

    return render(request, "users/profile.html", context)

def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.delete()
    messages.add_message(
                    request, messages.INFO, f"{request.user} вы успешно удалили заказ"
                )
    return HttpResponseRedirect(reverse("users:profile"))

def users_basket(request):
    return render(request, "users/users_basket.html")

@login_required
def logout(request):
    auth.logout(request)

    return HttpResponseRedirect(reverse("home"))