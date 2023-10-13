from django.contrib import admin

from . import models


admin.site.register(
    (
        models.BarmaidModel,
        models.CustomerModel,
        models.CourierModel,
        models.CartModel,
        models.UserModel
    )
)
