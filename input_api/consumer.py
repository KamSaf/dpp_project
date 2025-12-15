import json
import time
import pika
import requests
from pika.exceptions import AMQPConnectionError
from src.config import RABBIT_HOST, QUEUE_NAME, DB_API_HOST, DB_API_PORT
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
    print("Sending data to database...")
    url = f"http://{DB_API_HOST}:{DB_API_PORT}/save"
    data = {"img_url": data["img_url"], "ppl_num": ppl_num}
    while True:
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            print(f"[{response.status_code}] Data successfully saved to database!")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            break
        except requests.exceptions.RequestException as e:
            print("Couldn't send data to server endpoint. Trying again in 5 seconds", e)
            time.sleep(5)


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
