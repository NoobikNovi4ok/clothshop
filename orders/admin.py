from django.contrib import admin
from orders.models import Order, OrderItem

admin.site.register(OrderItem)


# admin.site.register(Order, OrderAdmin)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "created_timestamp",
        "status",
        "total_quantity",
        "cancellation_reason",
    )
    list_filter = ("status",)
    list_editable = ("status", "cancellation_reason")
    fields = ("user", "created_timestamp", "status", "cancellation_reason")
    readonly_fields = ("created_timestamp",)

    def total_quantity(self, obj):
        return obj.total_quantity()

    total_quantity.short_description = "Общее количество товаров"

    def save_model(self, request, obj, form, change):
        # Проверяем статус и только тогда изменяем причину отмены
        if obj.status == "Подтвержден":
            self.reduce_product_quantity(obj)
        elif obj.status == "Отменен" and not obj.cancellation_reason:
            obj.cancellation_reason = "Причина не указана"

        # Сохраняем объект
        super().save_model(request, obj, form, change)

    def reduce_product_quantity(self, order):
        for item in order.orderitem_set.all():
            product = item.product
            product.quantity -= item.quantity
            product.save()


admin.site.register(Order, OrderAdmin)
