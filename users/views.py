from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, RedirectView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import auth
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Prefetch
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, redirect
from orders.models import Order, OrderItem
from .forms import UserRegistrationForm, UserLoginForm


class UserRegistrationView(CreateView):
    template_name = "users/registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("users:profile")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        auth_user = authenticate(
            login=user.login, password=form.cleaned_data["password"]
        )

        if auth_user:
            login(self.request, auth_user)
            messages.success(self.request, f"{user} вы успешно вошли в аккаунт")
            return redirect(self.success_url)
        else:
            messages.error(self.request, "Ошибка аутентификации. Попробуйте еще раз.")
            return redirect(reverse_lazy("users:registration"))


class UserLoginView(LoginView):
    template_name = "users/login.html"
    form_class = UserLoginForm
    success_url = reverse_lazy("users:profile")
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, f"{user}, вы успешно вошли в аккаунт")
        return super().form_valid(form)

    def get_success_url(self):
        return self.success_url


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = (
            Order.objects.filter(user=self.request.user)
            .prefetch_related(
                Prefetch(
                    "orderitem_set",
                    queryset=OrderItem.objects.select_related("product"),
                )
            )
            .order_by("-id")
        )

        for order in orders:
            order.total_price = sum(
                item.products_price() for item in order.orderitem_set.all()
            )
        context["orders"] = orders
        context["title"] = "Профиль пользователя"
        return context


class DeleteOrderView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy("users:profile")

    def dispatch(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs["order_id"], user=request.user)
        order.delete()
        messages.add_message(
            request, messages.INFO, f"{request.user} вы успешно удалили заказ"
        )
        return super().dispatch(request, *args, **kwargs)


class UserBasketView(LoginRequiredMixin, TemplateView):
    template_name = "users/users_basket.html"


# class LogoutView(LoginRequiredMixin, RedirectView): #С выходом из аккаунта на страницу логина
#     url = reverse_lazy("home")

#     def dispatch(self, request, *args, **kwargs):
#         auth.logout(request)
#         return super().dispatch(request, *args, **kwargs)


class LogoutView(RedirectView):  # С выходом из аккаунта на главную страницу
    url = reverse_lazy("home")

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        auth.logout(request)
        return super().dispatch(request, *args, **kwargs)
