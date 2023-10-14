from django.shortcuts import render
from django.views import View
from django.http.request import HttpRequest


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
