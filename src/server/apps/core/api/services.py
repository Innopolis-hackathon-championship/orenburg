import json
import boto3


client = boto3.client(
        service_name='sqs',
        endpoint_url='https://message-queue.api.cloud.yandex.net',
        region_name='ru-central1',
        aws_access_key_id='YCAJEt98rsfo7c_4A1xHXpXSR',
        aws_secret_access_key='YCPs_6RLB-mSq3Jujp2EDjd0kiQ936raHA8qx1QE'
    )


def send_message_to_queue(msg, server=None):
    if server:
        msg['server'] = server

    client.send_message(
            QueueUrl="https://message-queue.api.cloud.yandex.net/b1gpldpf3veopdl8oo4c/dj600000000ptckq05ok/tg-msgs",
            MessageBody=json.dumps(msg)
        )
