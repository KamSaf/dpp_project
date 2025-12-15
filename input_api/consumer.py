import json
import time
import pika
from pika.exceptions import AMQPConnectionError
from src.config import RABBIT_HOST, QUEUE_NAME


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

    def callback(ch, method, _, body):
        data = json.loads(body)
        print(f"Task in progress...: {data}")
        time.sleep(5)
        print("Task completed!")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback,
        auto_ack=False,
    )

    print("Consumer running...")
    channel.start_consuming()


if __name__ == "__main__":
    main()
