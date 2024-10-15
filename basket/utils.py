from basket.models import Basket


def get_user_basket(request):
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
        return basket
    return None
