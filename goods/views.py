from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from goods.models import Cloths

class GoodsView(DetailView):
    template_name = "goods/cloth.html"
    slug_url_kwarg = "slug"
    model = Cloths
    context_object_name = "product"

    def get_object(self, queryset = None):
        return get_object_or_404(self.model, slug=self.kwargs.get(self.slug_url_kwarg))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['sizes'] = product.sizes.all()
        context['colors'] = product.colors.all()
        return context
