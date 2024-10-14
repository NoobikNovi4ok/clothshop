from django import template
from basket.models import Basket

register = template.Library()


@register.simple_tag()
def user_basket(request):
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
        return basket
