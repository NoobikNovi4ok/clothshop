from django.shortcuts import render
from goods.models import Categories, Countries, Cloths


def index(request):
    return render(request, "main/index.html")


def catalog(request):
    categories = Categories.objects.all()
    cloths = Cloths.objects.filter(quantity__gt=0)
    category_id = request.GET.get("category", 0)
    if category_id:
        cloths = Cloths.objects.filter(category=category_id)
    if category_id:
        context = {
            "cloths": cloths,
            "categories": categories,
            "category": category_id,
        }
    else:
        context = {"cloths": cloths, "categories": categories}

    return render(request, "main/catalog.html", context)


def contact(request):
    return render(request, "main/contact.html")
