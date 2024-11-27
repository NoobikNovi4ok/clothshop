from django.shortcuts import redirect
from django.db import transaction
from django.forms import ValidationError
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView
from basket.models import Basket
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem
from users.models import User


class CreateOrderView(LoginRequiredMixin, FormView):
    template_name = "orders/create_order.html"
    form_class = CreateOrderForm
    success_url = reverse_lazy("users:profile")

    def form_valid(self, form):
        login = form.cleaned_data["login"]
        password = form.cleaned_data["password"]
        user = User.objects.get(login=login)

        if user.check_password(password):
            try:
                with transaction.atomic():
                    user = self.request.user
                    cart_items = Basket.objects.filter(user=user)

                    if cart_items.exists():
                        order = Order.objects.create(user=user)
                        for cart_item in cart_items:
                            product = cart_item.cloth
                            price = cart_item.cloth.cost
                            quantity = cart_item.quantity

                            if product.quantity < quantity:
                                raise ValidationError(
                                    f"Недостаточное количество товара {product.name} на складе. В наличии - {product.quantity}"
                                )

                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                price=price,
                                quantity=quantity,
                            )
                            # product.quantity -= quantity
                            # product.save() #Для вычета до изменения статуса
                        cart_items.delete()
                        messages.success(self.request, "Заказ оформлен")

            except ValidationError as e:
                messages.error(self.request, str(e))
                return redirect("orders:create_order")
        else:
            messages.error(self.request, "Неверный пароль")
            return redirect("orders:create_order")

        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response({"form": form})
