from django.db import models

from goods.models import Cloths
from users.models import User


class OrderItemQuerySet(models.QuerySet):
    def total_price(self):
        return sum(basket.products_price() for basket in self)

    def total_quantity(self):
        if self:
            return sum(basket.quantity for basket in self)
        return 0


class Order(models.Model):
    user = models.ForeignKey(
        to=User, on_delete=models.SET_DEFAULT, verbose_name="Пользователь", default=None
    )
    created_timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания заказа"
    )
    status = models.CharField(
        max_length=50, default="В обработке", verbose_name="Статус заказа"
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ № {self.pk} | Покупатель {self.first_name} {self.last_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(
        to=Cloths,
        on_delete=models.SET_DEFAULT,
        null=True,
        verbose_name="Продукт",
        default=None,
    )
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    created_timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата продажи"
    )

    class Meta:
        verbose_name = "Проданный товар"
        verbose_name_plural = "Проданные товары"

    objects = OrderItemQuerySet.as_manager()

    def products_price(self):
        return round(self.price * self.quantity, 2)

    def __str__(self):
        return f"Товар {self.product.name} | Заказ № {self.order.pk}"
