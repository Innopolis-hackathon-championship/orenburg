"""
Обработчик сообщений

Получает сообщения из очереди и отправляет их в телеграм


Пример сообщения из очереди:
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


"""

import json
import os

import telebot

token = os.getenv("TELEGRAM_TOKEN")

bot = telebot.TeleBot(token, parse_mode=None)


settings_ = {
    "test": {
        "server": "https://0.0.0.0:3000",
    },
    'test2': {
        "server": "https://10.242.26.31:3000",
    }
}

settings = settings_['test2']


def handle_process_event(event, context):

    for message in event['messages']:
        task_json = json.loads(message['details']['message']['body'])

        if "server" not in task_json:
            task_json['server'] = settings['server']
      
        server = task_json['server']
        del task_json['server'] 

        match list(task_json.keys())[0]:
            case 'sendMessege':
                
                btns = []

                task = task_json['sendMessege']
                tg_user_id = task['userId']

                msg = task['message']

                if "buttons" in task:
                    print(task['buttons'])
                    for btn in task['buttons']:
                        match list(btn.keys())[0]:
                            case "order":
                                btns.append([telebot.types.InlineKeyboardButton(text="Посмотреть заказ", web_app=telebot.types.WebAppInfo(f'{server}/order/' + btn['order']))])
                            case "feedback":
                                btns.append([telebot.types.InlineKeyboardButton(text="Оставить отзыв", web_app=telebot.types.WebAppInfo(f'{server}/feedback/' + btn['feedback'])),])
                                btns.append([
                                    telebot.types.InlineKeyboardButton(text="1️⃣⭐️", callback_data=f"rate:{btn['feedback']}:1"),
                                    telebot.types.InlineKeyboardButton(text="2️⃣⭐️", callback_data=f"rate:{btn['feedback']}:2"),
                                    telebot.types.InlineKeyboardButton(text="3️⃣⭐️", callback_data=f"rate:{btn['feedback']}:3"),
                                    telebot.types.InlineKeyboardButton(text="4️⃣⭐️", callback_data=f"rate:{btn['feedback']}:4"),
                                    telebot.types.InlineKeyboardButton(text="5️⃣⭐️", callback_data=f"rate:{btn['feedback']}:5"),
                                ])
                            case "link":
                                btns.append([telebot.types.InlineKeyboardButton(text="Перейти", url=btn['link'])])
                            case "callback":
                                btns.append([telebot.types.InlineKeyboardButton(text="Перейти", callback_data=btn['callback'])])
                            case "web_app":
                                btns.append([telebot.types.InlineKeyboardButton(text="Открыть", web_app=telebot.types.WebAppInfo(btn['web_app']))])



                bot.send_message(tg_user_id, msg, reply_markup=telebot.types.InlineKeyboardMarkup(btns))


    return "OK"