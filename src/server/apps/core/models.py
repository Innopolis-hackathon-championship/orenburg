from django.db import models
from django.utils import timezone


def product_image_upload_path(instance, filename):
    return 'product_images/{}'.format(filename)


class ProductModel(models.Model):
    name = models.CharField(
        "Название", max_length=127
    )
    quantity = models.IntegerField(
        "Количество", default=0
    )
    price = models.FloatField(
        "Цена", default=0
    )

    image = models.ImageField(
        upload_to=product_image_upload_path,
        max_length=511,
        default="product_images/Заглушка фото карточки товара.png",
        verbose_name="Выбрать изображение"
    )
    
    is_visible = models.BooleanField(
        "Отображается?",
        default=True
    )
    
    class Meta:
        db_table = "product"
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        
    def __str__(self) -> str:
        return f"{self.name}({self.quantity})"


class OrderModel(models.Model):
    customer_id = models.IntegerField()
    status = models.CharField(
        "Статус", max_length=12,
        choices=(
            ("prepare", "Готовится"),
            ("ready", "Ожидает доставки"),
            ("delivery", "Доставляется"),
            ("arrived", "Ожидание"),
            ("finished", "Завершен"),
        ),
        default="prepare"
    )
    delivery_address = models.CharField(
        "Адрес доставки", max_length=127,
        null=True, blank=True
    )
    courier_id = models.IntegerField(
        null=True, blank=True
    )
    delivery_start_date = models.DateTimeField(
        null=True, blank=True
    )
    
    start_date = models.DateTimeField(
        "Дата заказа", default=timezone.now
    )
    finish_date = models.DateTimeField(
        "Дата получения", default=None,
        null=True, blank=True
    )
    
    amount = models.IntegerField(
        "Стоимость", default=0
    )
    
    code = models.CharField(
        "Код", max_length=6
    )
    
    class Meta:
        db_table = "order"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
    
    products = models.ManyToManyField(
        ProductModel,
        through="OrderToProductModel",
        verbose_name="Продукты"
    )
    
    def __str__(self) -> str:
        return f"{self.pk}: {self.amount}"
    

class OrderToProductModel(models.Model):
    order = models.ForeignKey(
        OrderModel,
        verbose_name="Заказ",
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        ProductModel,
        verbose_name="Продукт",
        on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField(
        "Количество", default=0
    )

    class Meta:
        db_table = "product_to_order"
        verbose_name = "Заказ к товару"
        verbose_name_plural = "Заказы к товарам"
        unique_together = ('order', 'product')
    
    def __str__(self) -> str:
        return f"{self.product.name} - {self.amount}"
    
    
class DeliveryQueueModel(models.Model):
    order_id = models.IntegerField(unique=True)
    queue = models.TextField()
    pointer = models.IntegerField()
    last_offer_date = models.DateField(
        default=timezone.now
    )

    class Meta:
        db_table = "delivery_queue"
        verbose_name = "Очередь заказов"
        verbose_name_plural = "Очереди заказов"
    
    def __str__(self) -> str:
        return f"{self.order_id} {self.queue} pointer: {self.pointer}"


class CourierModel(models.Model):
    is_online = models.BooleanField('is_online', default=False)
    raiting = models.FloatField("raiting", default=5)
    is_delivering = models.BooleanField("is_delivering", default=False)

    class Meta:
        db_table = "courier"
        verbose_name = "Курьер"
        verbose_name_plural = "Курьеры"
