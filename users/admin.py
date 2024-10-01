from django.contrib import admin
from users.models import User


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ["name", "surname", "login", "email", "is_staff", "is_active"]
#     search_fields = ["surname", "login", "email", "is_staff"]

#     def user_display(self, obj):
#         if obj.user:
#             return str(obj.user)


class UserAdmin(admin.ModelAdmin):
    # Указываем поля, которые будут отображаться в форме
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "login",
                    "name",
                    "surname",
                    "patronymic",
                    "is_active",
                    "is_staff",
                )
            },
        ),
    )

    # Указываем, какие поля будут отображаться в списке пользователей
    list_display = ("email", "login", "name", "surname", "is_active", "is_staff")

    # Исключаем группы и разрешения
    exclude = ("groups", "user_permissions")


# Регистрируем модель пользователя с нашим классом администратора
admin.site.register(User, UserAdmin)
