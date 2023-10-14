import json

from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.request import Request
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.db.models import Q

from .. import models
from api.profiles.models import UserModel
from .services import send_message_to_queue
from . import serializers


class TakeDeliveryView(APIView):
    serializer_class = serializers.ProductSerializer
    permission_classes = [AllowAny]

    def get(self, request: Request):
        serializer = self.serializer_class(
            models.ProductModel.objects.all(),
            many=True
        )
        
        return Response(
            serializer.data,
            status.HTTP_200_OK
        )

    def post(self, request: Request):
        for product in request.data:
            instance = models.ProductModel.objects.get(pk=product["id"])
            
            serializer = self.serializer_class(
                instance, data=product
            )
            
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status.HTTP_400_BAD_REQUEST
                )
            
            serializer.save()
        
        return Response({
            "message": "ok"
        }, status.HTTP_200_OK)


class NewOrdersView(generics.ListAPIView):
    queryset = models.OrderModel.objects.filter(
        status__in=["prepare", "ready", "wait", "waitcourier"]
    )
    serializer_class = serializers.OrderSerializer
    

class DeliveryStatusView(APIView):
    def get(self, request: Request):
        order_id = request.query_params.get("order_id")
        
        queue = models.DeliveryQueueModel.objects.filter(
            order_id=order_id
        ).first()
        
        if queue:
            return Response({
                "message": "courier finding"
            }, status.HTTP_200_OK)
        
        return Response({
            "message": "No courier"
        }, status.HTTP_404_NOT_FOUND)


class FindDeliveryView(APIView):
    def get(self, request: Request):
        order_id = request.query_params.get("order_id")
        
        if not order_id:
            return Response({
                "message": "no order_id in query params"
            }, status.HTTP_400_BAD_REQUEST)
            
        order = models.OrderModel.objects.filter(
            pk=order_id
        ).first()
    
        if not order:
            return Response({
                "message": f"no order by {order_id} id"
            }, status.HTTP_400_BAD_REQUEST)
        
        queue = models.DeliveryQueueModel.objects.filter(
            order_id=order_id
        ).first()
        
        if queue:
            if len(json.loads(queue.queue)) > queue.pointer + 1:
                queue.pointer += 1
                queue.save()
                
                telegram_id = json.loads(queue.queue)[queue.pointer]
            else:
                order.status = "prepare"
                order.save()

                queue.delete()
                
                return Response({
                    "message": "No couriers online"
                }, status.HTTP_200_OK)
        else:
            couriers = UserModel.objects.filter(
                role="courier"
            ).values_list("pk", flat=True)

            couriers = models.CourierModel.objects.filter(
                is_online=True,
                pk__in=couriers
            ).order_by("-raiting").values_list("pk", flat=True)
            
            queue = []
            
            for courier in couriers:
                user = UserModel.objects.filter(
                    pk=courier
                ).first()
                
                if not user:
                    continue
                    
                queue.append(user.telegram_id)
            
            if not queue:
                return Response({
                    "message": "No courier queue"
                }, status.HTTP_404_NOT_FOUND)
            
            delivery_queue = models.DeliveryQueueModel.objects.create(
                order_id=order_id,
                queue=json.dumps(queue),
                pointer=0
            )

            telegram_id = queue[0]
        
        if order.status == "prepare":
            order.status = "ready"
            order.save()
            
        send_message_to_queue({
            "sendMessege": {
                "userId": telegram_id,
                "message": f"Вам пришла новая заявка!\nМесто доставки: {order.delivery_address}",
                "buttons": [
                    {
                        "courier_offer": f"{order_id}",
                    }
                ]
            }
        })

        return Response({
            "message": "Finding courier"
        }, status.HTTP_200_OK)


class TakeReadyDeliveryView(APIView):
    def get(self, request: Request):
        order_id = request.query_params.get("order_id")
        telegram_id = request.query_params.get("telegram_id")
        
        user = UserModel.objects.filter(
            telegram_id=telegram_id
        ).first()
        
        if not user:
            return Response({
                "message": f"No user with {telegram_id} telegram id"
            })

        if user.role != "courier":
            return Response({
                "message": f"User not courier"
            })
        
        courier_instance = models.CourierModel.objects.filter(
            pk=user.pk
        ).first()
        
        if not courier_instance:
            models.CourierModel.objects.create(
                id=user.pk,
                is_online=False,
                raiting=5
            )
        
        if not order_id:
            return Response({
                "message": "no order_id in query params"
            }, status.HTTP_200_OK)
        
        order = models.OrderModel.objects.filter(
            pk=order_id
        ).first()

        if not order:
            return Response({
                "message": f"no order by {order_id} id"
            }, status.HTTP_400_BAD_REQUEST)        

        queue = models.DeliveryQueueModel.objects.filter(
            order_id=order_id
        ).first()
        
        if queue:
            queue.delete()
            
        order.status = "waitcourier"
        order.courier_id = user.pk

        order.save()

        courier_instance.is_online = False
        courier_instance.is_delivering = True
        courier_instance.save()

        return Response({
            "delivery_address": order.delivery_address,
            "code": order.code
        }, status.HTTP_200_OK)

        
class GiveDeliveryView(APIView):
    def get(self, request: Request):
        order_id = request.query_params.get("order_id")
        
        if not order_id:
            return Response({
                "message": "no order_id in query params"
            }, status.HTTP_400_BAD_REQUEST)
            
        order = models.OrderModel.objects.filter(
            pk=order_id
        ).first()
    
        if not order:
            return Response({
                "message": f"no order by {order_id} id"
            }, status.HTTP_400_BAD_REQUEST)
            
        order.status = "delivery"
        order.delivery_start_date = timezone.now()

        order.save()
        
        return Response({
            "message": "ok"
        }, status.HTTP_200_OK)


class OrderReadyView(APIView):
    def get(self, request: Request):
        order_id = request.query_params.get("order_id")
        
        if not order_id:
            return Response({
                "message": "no order_id in query params"
            }, status.HTTP_400_BAD_REQUEST)
            
        order = models.OrderModel.objects.filter(
            pk=order_id
        ).first()
    
        if not order:
            return Response({
                "message": f"no order by {order_id} id"
            }, status.HTTP_400_BAD_REQUEST)
            
        user = UserModel.objects.filter(
            pk=order.customer_id
        ).first()
        
        if not user:
            order.delete()
            return Response({
                "message": "no user"
            }, status.HTTP_400_BAD_REQUEST)
            
        order.status = "wait"
        order.save()
        
        send_message_to_queue({
            "sendMessege": {
                "userId": user.telegram_id,
                "message": f"Ваш заказ готов!\nМожете получить его по следующему PIN коду: {order.code}",
            }
        })
        
        return Response({
            "message": "ok"
        }, status.HTTP_200_OK)


class OrderTakeView(APIView):
    def get(self, request: Request):
        order_id = request.query_params.get("order_id")
        
        if not order_id:
            return Response({
                "message": "no order_id in query params"
            }, status.HTTP_400_BAD_REQUEST)
            
        order = models.OrderModel.objects.filter(
            pk=order_id
        ).first()
    
        if not order:
            return Response({
                "message": f"no order by {order_id} id"
            }, status.HTTP_400_BAD_REQUEST)

        order.status = "finished"
        order.finish_date = timezone.now()
        
        user = UserModel.objects.filter(pk=order.customer_id).first()
        
        if not user:
            order.delete()

            return Response({
                "message": "no user"
            }, status.HTTP_200_OK)
        
        user.balance -= order.amount
        user.save()
        
        if order.courier_id:
            courier = models.CourierModel.objects.filter(
                pk=order.courier_id
            ).first()

            if courier:
                courier.is_online = True
                courier.is_delivering = False
                
                courier.save()
                
                user_courier = UserModel.objects.filter(
                    pk=order.courier_id
                ).first()
                
                if user_courier:
                    user_courier.balance += order.amount // 10
                    user_courier.save()
        
        m2m = models.OrderToProductModel.objects.filter(
            order=order_id
        )
        
        for m in m2m:
            product = models.ProductModel.objects.filter(
                pk=m.product.pk
            ).first()
            
            if product:
                product.quantity -= m.amount
                product.save()

        order.delete()
        
        return Response({
            "message": "ok"
        }, status.HTTP_200_OK)


class DeliveryArrivedView(APIView):
    def get(self, request: Request):
        order_id = request.query_params.get("order_id")
        
        if not order_id:
            return Response({
                "message": "no order_id in query params"
            }, status.HTTP_400_BAD_REQUEST)
            
        order = models.OrderModel.objects.filter(
            pk=order_id
        ).first()
    
        if not order:
            return Response({
                "message": f"no order by {order_id} id"
            }, status.HTTP_400_BAD_REQUEST)
        
        order.status = "arrived"
        order.save()
        
        user = UserModel.objects.filter(
            pk=order.customer_id
        ).first()
        
        if not user:
            return Response({
                "message": "not user"
            }, status.HTTP_400_BAD_REQUEST)
        
        send_message_to_queue({
            "sendMessege": {
                "userId": user.telegram_id,
                "message": f"Подтвердите получение заказа!\nPIN код для подверждения: {order.code}",
                "buttons": [
                    {
                        "comfirm": order_id
                    },
                ]
            }
        })
        
        return Response({
            "message": "ok"
        }, status.HTTP_200_OK)
