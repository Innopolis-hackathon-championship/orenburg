from django.contrib import admin

from . import models


admin.site.register((
    models.ProductModel,
    models.OrderModel,
    models.OrderToProductModel
))
