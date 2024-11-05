from django.urls import path
from main import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="home"),
    path("catalog", views.CatalogView.as_view(), name="catalog"),
    path("contact", views.ContactView.as_view(), name="contact"),
]
