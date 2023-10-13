from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.views import View
from django.http.request import HttpRequest

from api.profiles import models as profile_models
from api.products import models as products_models
from api.orders import models as order_models


class IndexView(View):
    def get(self, request: HttpRequest):
        return render(
            request,
            "core/index.html"
        )


class TakeDeliveryView(View):
    def get(self, request: HttpRequest):
        return render(
            request,
            "core/take_delivery.html"
        )
