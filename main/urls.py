from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.index, name="home"),
    path("catalog", views.catalog, name="catalog"),
    path("contact", views.contact, name="contact"),
    path("user/", include("users.urls", namespace="user")),
]
