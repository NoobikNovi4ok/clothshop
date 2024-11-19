from basket.models import Basket


def get_user_basket(request):
    if request.user.is_authenticated:
        return Basket.objects.filter(user=request.user).select_related("cloth")

    return None
