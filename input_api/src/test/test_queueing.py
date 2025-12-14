import time
import json
import pytest
import pika
from src.test.config import client, TEST_RABBIT_HOST, TEST_QUEUE_NAME


@pytest.fixture(scope="module")
def rabbit_connection():
    for _ in range(10):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=TEST_RABBIT_HOST)
            )
            channel = connection.channel()
            channel.queue_declare(queue=TEST_QUEUE_NAME)
            return connection
        except Exception:
            time.sleep(1)
    raise RuntimeError("RabbitMQ not running")


def test_queueing(rabbit_connection):
    payload = {"img_url": "test_image_url"}
    response = client.post("/enqueue", json=payload)
    assert response.status_code == 201

    channel = rabbit_connection.channel()
    method_frame, header_frame, body = channel.basic_get(
        TEST_QUEUE_NAME, auto_ack=False
    )
    assert method_frame is not None

    task = json.loads(body)
    assert task["img_url"] == payload["img_url"]

    rabbit_connection.close()
