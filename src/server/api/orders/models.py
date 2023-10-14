from django.db import models
from django.utils import timezone

from api.profiles import models as profile_models
from api.products import models as product_models


class OrderModel(models.Model):
    class OrderStatusChoices(models.TextChoices):
        CREATED = "created", "Создан"
        BAKED = "baked", "Готовится"
        IN_DELIVERY = "in_delivery", "В доставке"
        RECEIVED = "received", "Получен"

    user = models.ForeignKey(
        profile_models.UserModel, models.CASCADE,
        verbose_name="Пользователь"
    )
    
    delivery_address = models.CharField(
        "Адрес доставки", max_length=511,
        null=True, blank=True
    )
    
    status = models.CharField(
        "Статус", max_length=32,
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.CREATED
    )
    
    start_date = models.DateTimeField(
        "Дата заказа", default=timezone.now
    )
    end_date = models.DateTimeField(
        "Дата получения", default=None,
        null=True, blank=True
    )
    
    amount = models.IntegerField(
        "Стоимость", default=0
    )
    
    products = models.ManyToManyField(
        product_models.ProductModel,
        through="Order2ProductModel",
        verbose_name="Продукты"
    )
    
    class Meta:
        db_table = "order__order"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
    
    def __str__(self) -> str:
        return f"{self.pk}: {self.user.fullname} {self.amount}"


class Order2ProductModel(models.Model):
    order = models.ForeignKey(
        OrderModel,
        verbose_name="Заказ",
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        product_models.ProductModel,
        verbose_name="Модификация продукта",
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(
        "Количество", default=0
    )

    class Meta:
        db_table = "order__order2modification"
        verbose_name = "Заказ к модификации товара"
        verbose_name_plural = "Заказ к модификациям товаров"
        unique_together = ('order', 'product')
    
    def __str__(self) -> str:
        return f"{self.product.name} - {self.quantity}"
