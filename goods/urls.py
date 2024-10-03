from django.urls import path

from goods.views import goods_get

urlpatterns = [
    path(r"<slug:slug>", goods_get),
]
