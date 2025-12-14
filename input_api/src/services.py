import pika
import json
from src.config import RABBIT_HOST, QUEUE_NAME


def create_task(url: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)

    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=json.dumps({"img_url": url}),
    )
    connection.close()
