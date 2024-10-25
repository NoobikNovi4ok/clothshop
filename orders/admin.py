from django.contrib import admin
from django import forms

from orders.models import Order, OrderItem

admin.site.register(OrderItem)


# admin.site.register(Order, OrderAdmin)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_timestamp', 'status','total_quantity', 'cancellation_reason')
    list_filter = ('status',)
    list_editable = ('status', 'cancellation_reason')
    fields = ('user', 'created_timestamp', 'status', 'cancellation_reason')
    readonly_fields = ('created_timestamp',)

    def total_quantity(self, obj):
        return obj.total_quantity()
    total_quantity.short_description = 'Общее количество товаров'  

    def save_model(self, request, obj, form, change):
        # Проверяем статус и только тогда изменяем причину отмены
        if obj.status == "Новый":
            obj.cancellation_reason = "Новый заказ"
        elif obj.status == "Подтвержден":
            obj.cancellation_reason = "Заказ был подтвержден"
        elif obj.status == "Отменен" and not obj.cancellation_reason:
            obj.cancellation_reason = "Причина не указана"
        
        # Сохраняем объект
        super().save_model(request, obj, form, change)
    

admin.site.register(Order, OrderAdmin)