from django.urls import path
from users.views import UserLoginView, registration, users_basket, profile, logout, delete_order


app_name = "users"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("registration/", registration, name="registration"),
    path("users-basket", users_basket, name="users-basket"),
    path("profile/", profile, name="profile"),
    path("logout/", logout, name="logout"),
    path('delete_order/<int:order_id>/', delete_order, name='delete_order')
]
