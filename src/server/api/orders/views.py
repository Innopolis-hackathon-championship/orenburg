from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.conf import settings


class TestView(APIView):
    def get(self, request: Request):
        return Response(
            [
            {
                "delivery_address": None,
                "products": [
                    {
                        "quantity": 2,
                        "product": {
                            "name": "Bulka",
                            "image": "http://2.bp.blogspot.com/-d3BCIYnJcSg/UBjvvSee2TI/AAAAAAAAAKM/CzYoimr2KDg/s1600/karas.jpg",
                            "price": 1000.0
                        },
                    },
                    {
                        "quantity": 1,
                        "product": {
                            "name": "Pivo",
                            "image": "http://2.bp.blogspot.com/-d3BCIYnJcSg/UBjvvSee2TI/AAAAAAAAAKM/CzYoimr2KDg/s1600/karas.jpg",
                            "price": 1000.0
                        },
                    }
                ],
            },
            {
                "delivery_address": "кабинет 310",
                "products": [
                    {
                        "quantity": 4,
                        "product": {
                            "name": "Bulka",
                            "image": "http://2.bp.blogspot.com/-d3BCIYnJcSg/UBjvvSee2TI/AAAAAAAAAKM/CzYoimr2KDg/s1600/karas.jpg",
                            "price": 1000.0
                        },
                    },
                    {
                        "quantity": 3,
                        "product": {
                            "name": "Pivo",
                            "image": "http://2.bp.blogspot.com/-d3BCIYnJcSg/UBjvvSee2TI/AAAAAAAAAKM/CzYoimr2KDg/s1600/karas.jpg",
                            "price": 1000.0
                        },
                    }
                ],
            }
        ],
            status.HTTP_200_OK
        )
