from django.urls import path
from users.views import login, registration, users_basket


app_name = "users"

urlpatterns = [
    path("login/", login, name="login"),
    path("registration/", registration, name="registration"),
    path("users-basket", users_basket, name="users-basket"),
]
