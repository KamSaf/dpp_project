import json
import time
import pika
from pika.exceptions import AMQPConnectionError
from src.config import RABBIT_HOST, QUEUE_NAME
from src.object_detection import process_img
from src.utils import load_image_from_url


def callback(ch, method, _, body):
    data = json.loads(body)
    img = load_image_from_url(data["img_url"])
    if img is None:
        print(f"Cannot process image from given URL.: {data['img_url']}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return
    print(f"Task in progress...: {data['img_url']}")
    ppl_num = process_img(img)
    print(f"Task completed! Number of people detected: {ppl_num}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBIT_HOST)
            )
            print("RabbitMQ connected.")
            break
        except AMQPConnectionError:
            print("Awaiting RabbitMQ connection...")
            time.sleep(2)

    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)

    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback,
        auto_ack=False,
    )

    print("Consumer running...")
    channel.start_consuming()


if __name__ == "__main__":
    main()
