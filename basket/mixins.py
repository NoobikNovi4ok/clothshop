from django.template.loader import render_to_string
from django.urls import reverse
from basket.models import Basket
from basket.utils import get_user_basket


class BasketMixin:
    def get_cart(self, request, product=None, cart_id=None):
        query_kwargs = {"user": request.user}

        if product:
            query_kwargs["cloth"] = product
        if cart_id:
            query_kwargs["basket_id"] = cart_id

        return Basket.objects.filter(**query_kwargs).first()

    def render_cart(self, request):
        user_basket = get_user_basket(request)

        context = {
            "basket": user_basket,
        }

        return render_to_string(
            "basket/includes/included_cart.html",
            context,
            request=request,
        )
