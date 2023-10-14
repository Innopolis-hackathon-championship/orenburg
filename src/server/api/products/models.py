from django.db import models


def product_image_upload_path(instance, filename):
    return 'product_images/{}/{}'.format(instance.product_id, filename)


class ProductModel(models.Model):
    name = models.CharField(
        "Название", max_length=255
    )    
    price = models.FloatField(
        "Цена"
    )
    quantity = models.IntegerField(
        "Количество", default=0
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
        db_table = "product__product"
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        
    def __str__(self) -> str:
        return f"{self.name}"
