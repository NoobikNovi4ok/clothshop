from django.urls import path
from users.views import (
    DeleteOrderView,
    ProfileView,
    UserLoginView,
    UserRegistrationView,
    UserBasketView,
    LogoutView,
)


app_name = "users"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("registration/", UserRegistrationView.as_view(), name="registration"),
    path("users-basket", UserBasketView.as_view(), name="users-basket"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "delete_order/<int:order_id>/", DeleteOrderView.as_view(), name="delete_order"
    ),
]
