# Generated by Django 4.2.6 on 2023-10-14 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_ordermodel"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ordermodel",
            name="status",
            field=models.CharField(
                choices=[
                    ("prepare", "Готовится"),
                    ("delivery", "Доставляется"),
                    ("arrived", "Ожидание"),
                    ("finished", "Завершен"),
                ],
                default="prepare",
                max_length=12,
                verbose_name="Статус",
            ),
        ),
        migrations.CreateModel(
            name="Order2ProductModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "quantity",
                    models.PositiveIntegerField(default=0, verbose_name="Количество"),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.ordermodel",
                        verbose_name="Заказ",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.productmodel",
                        verbose_name="Продукт",
                    ),
                ),
            ],
            options={
                "verbose_name": "Заказ к товару",
                "verbose_name_plural": "Заказы к товарам",
                "db_table": "product_to_order",
                "unique_together": {("order", "product")},
            },
        ),
    ]
