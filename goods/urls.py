from django.urls import path

from goods import views

urlpatterns = [
    path(r"<slug:slug>", views.GoodsView.as_view()),
]
