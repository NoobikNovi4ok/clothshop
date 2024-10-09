from django.contrib import admin
from goods.models import Size, Color, Cloths, Categories, Countries


@admin.register(Cloths)
class ClothsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Countries)
class CountriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Size)
admin.site.register(Color)
