from django.contrib import admin
from django.contrib.auth.models import Group

from . import models


# admin.site.register(
#     (
#         models.BarmaidModel,
#         models.CustomerModel,
#         models.CourierModel,
#         models.CartModel,
#         models.UserModel
#     )
# )

admin.site.unregister(Group)
