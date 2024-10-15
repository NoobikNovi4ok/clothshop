from django.contrib import admin
from basket.models import Basket


@admin.register(Basket)
class UserAdmin(admin.ModelAdmin):
    list_display = ["user", "basket_id", "cloth"]
    search_fields = ["user", "basket_id"]
