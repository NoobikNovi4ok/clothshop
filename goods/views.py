from django.shortcuts import render
from goods.models import Cloths


def goods_get(request, slug):
    cloth = Cloths.objects.get(slug=slug)
    context = {
        "product": cloth,
    }
    render(request, "goods/cloth.html", context)
