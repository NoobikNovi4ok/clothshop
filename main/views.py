from django.db.models import Q
from django.shortcuts import render
from goods.models import Categories, Countries, Cloths


def index(request):
    return render(request, "main/index.html")


# def catalog(request):
#     categories = Categories.objects.all()
#     cloths = Cloths.objects.filter(quantity__gt=0)
#     category_slug = request.GET.get("category", 0)
#     if category_slug:
#         category = Categories.objects.get(slug=category_slug)
#         print(category)
#         print(category.id)
#         shmot = Cloths.objects.filter(category=category.id)
#         print(shmot)
#         if shmot:
#             context = {
#                 "cloths": shmot,
#                 "categories": categories,
#                 "category": category,
#             }
#             return render(request, "main/catalog.html", context)
#         else:
#             context = {"categories": categories}
#     else:
#         context = {
#             "cloths": cloths,
#             "categories": categories,
#         }
#     return render(request, "main/catalog.html", context)


def catalog(request):
    cloths = Cloths.objects.filter(quantity__gt=0)  # Показываем только доступные товары
    categories = Categories.objects.all()
    reguest = request.GET.getlist('sort')
    categorya = None

    # Фильтрация по категории
    category_slug = request.GET.getlist("category", 0)
    if category_slug:
        categorya = Categories.objects.filter(slug__in=category_slug)
        cloths = cloths.filter(category__in=categorya)


    # Сортировка
    sort_by = request.GET.get("sort", "newest")
    cloths = cloths.order_by("-pk")
    if sort_by == "year":
        cloths = cloths.order_by("-year")
    elif sort_by == "name":
        cloths = cloths.order_by("name")
    elif sort_by == "price":
        cloths = cloths.order_by("cost")

    if categorya is not None:
        context = {
            "select_category":categorya,
            "cloths": cloths,
            "categories": categories,
            "selected_category": category_slug,
            "selected_sort": sort_by,
            "request": reguest,
        }
    else:
        context = {
            "cloths": cloths,
            "categories": categories,
            "selected_category": category_slug,
            "selected_sort": sort_by,
            "request": reguest,
        }
    return render(request, "main/catalog.html", context)


def contact(request):
    return render(request, "main/contact.html")
