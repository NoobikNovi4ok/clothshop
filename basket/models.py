from django.db import models
from users.models import User
from goods.models import Cloths


class BasketQuerySet(models.QuerySet):
    def total_price(self):
        return sum(basket.products_price() for basket in self)

    def total_quantity(self):
        if self:
            return sum(basket.quantity for basket in self)
        return 0


class Basket(models.Model):
    basket_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        to=User, on_delete=models.PROTECT, verbose_name="Пользователь"
    )
    cloth = models.ForeignKey(
        to=Cloths, on_delete=models.PROTECT, verbose_name="Продукт"
    )
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    created_timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата добавления"
    )

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"

    objects = BasketQuerySet().as_manager()

    def products_price(self):
        return round(self.cloth.cost * self.quantity, 2)

    def __str__(self):
        return f"Корзина {self.user.login} | Товар {self.cloth.name} | Количество {self.quantity}"
