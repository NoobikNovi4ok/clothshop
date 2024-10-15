from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import transaction
from basket.models import Basket
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem
from django.forms import ValidationError
from django.contrib import messages


@login_required
def create_order(request):
    if request.method == "POST":
        form = CreateOrderForm(data=request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = request.user
                    cart_items = Basket.objects.filter(user=user)

                    if cart_items.exists():
                        order = Order.objects.create(
                            user=user,
                            first_name=form.cleaned_data["first_name"],
                            last_name=form.cleaned_data["last_name"],
                            phone_number=form.cleaned_data["phone_number"],
                        )
                        for cart_item in cart_items:
                            product = cart_item.product
                            price = cart_item.product.cost
                            quantity = cart_item.quantity

                            if product.quantity < quantity:
                                raise ValidationError(
                                    f"Недостаточное количество товара {product.name} на складе\
                                                        В наличии - {product.quantity}"
                                )

                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                price=price,
                                quantity=quantity,
                            )
                            product.quantity -= quantity
                            product.save()

                        cart_items.delete()

                        messages.success(request, "Заказ оформлен")
                        return redirect("user:profile")
            except ValidationError as e:
                messages.success(request, str(e))
                return redirect("orders:create_orders")
    else:
        form = CreateOrderForm()

    context = {"form": form}
    return render(request, "orders/create_order.html", context=context)
