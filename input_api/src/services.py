import pika
import json
from src.config import RABBIT_HOST, QUEUE_NAME


def create_task(url: str):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBIT_HOST if RABBIT_HOST else "rabbitmq")
    )
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)

    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME if QUEUE_NAME else "img_queue",
        body=json.dumps({"url": url}),
    )
    connection.close()
