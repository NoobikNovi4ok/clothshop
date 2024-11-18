from django.views.generic import TemplateView, ListView
from goods.models import Categories, Cloths


class IndexView(TemplateView):
    template_name = "main/index.html"


class CatalogView(ListView):
    model = Cloths
    context_object_name = "cloths"
    template_name = "main/catalog.html"
    paginate_by = 1
    allow_empty = False

    def get_queryset(self):
        cloths = super().get_queryset().filter(quantity__gt=0).order_by("-pk")
        # Фильтрация по категории
        category_slug = self.request.GET.getlist("category", [])
        if category_slug:
            categorya = Categories.objects.filter(slug__in=category_slug)
            cloths = cloths.filter(category__in=categorya)
        # Сортировка
        sort_by = self.request.GET.get("sort", "newest")
        if sort_by == "year":
            cloths = cloths.order_by("-year")
        elif sort_by == "name":
            cloths = cloths.order_by("name")
        elif sort_by == "price":
            cloths = cloths.order_by("cost")
        return cloths

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categories"] = Categories.objects.all()
        context["get_slug_category"] = self.request.GET.getlist("category", [])
        context["select_category"] = Categories.objects.filter(
            slug__in=context["get_slug_category"]
        )
        context["selected_sort"] = self.request.GET.get("sort", "newest")
        return context


class ContactView(TemplateView):
    template_name = "main/contact.html"
