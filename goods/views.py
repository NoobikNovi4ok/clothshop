from django.shortcuts import render
from goods.models import Cloths


def goods_get(request, slug):
    cloth = Cloths.objects.get(slug=slug)
    sizes = cloth.sizes.all()
    colors = cloth.colors.all()
    context = {
        "product": cloth,
        'sizes': sizes,
        'colors': colors,
    }
    return render(request, "goods/cloth.html", context)
