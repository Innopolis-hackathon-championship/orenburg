import json
import os

import boto3

client = boto3.client(
        service_name='sqs',
        endpoint_url='https://message-queue.api.cloud.yandex.net',
        region_name='ru-central1',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )

def send_message_to_queue(msg, server=None):
    """
    Отправка сообщения в очередь

    Пример сообщения:
    ```json
    {
        "sendMessege": {
            "userId": 123456789,
            "message": "Ваш заказ №123456789 доставлен 🎉",
            "buttons": [
                {
                    "order": "order_id"
                },
                {
                    "feedback": "order_id",
                }
            ]
        }
    }
    ```

    Доступные типы кнопок:
    - order - Переход на страницу заказа
    - feedback - Оставить отзыв
    - link - Переход по ссылке
    - callback - Колбек кнопка
    - web_app - Открыть веб приложение
        
        ```json
        {
            "sendMessege": {
                "userId": 123456789,
                "message": "Ваш заказ №123456789 доставлен 🎉",
                "buttons": [
                    {
                        "order": "123456789"
                    },
                    {
                        "feedback": "true",
                    },
                    {
                        "link": "https://google.com"
                    },
                    {
                        "callback": "callback_data"
                    },
                    {
                        "web_app": "https://google.com"
                    }
                ]
            }
        }
        ```

        Так же можно указать сервер, на котором запущено веб приложение

    """
    if server:
        msg['server'] = server

    client.send_message(
            QueueUrl=os.getenv("QUEUE_URL"),
            MessageBody=json.dumps(msg)
        )


if __name__ == '__main__':

    send_message_to_queue({
        "sendMessege": {
            "userId": 493431536,
            "message": "Ваш заказ №123456789 доставлен 🎉",
            "buttons": [
                {
                    "order": "123"
                },
                {
                    "feedback": "123",
                },
                
            ]
        }
    })