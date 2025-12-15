import json
import os
import pika
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

TEST_RABBIT_HOST = os.getenv("TEST_RABBIT_HOST", "localhost")
TEST_QUEUE_NAME = os.getenv("TEST_QUEUE_NAME", "img_queue")


@pytest.fixture
def rabbit_connection():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=TEST_RABBIT_HOST)
    )
    channel = connection.channel()
    channel.queue_declare(queue=TEST_QUEUE_NAME)
    yield channel
    channel.queue_purge(queue=TEST_QUEUE_NAME)
    connection.close()


def test_enqueue_task(rabbit_connection):
    test_data = {"img_url": "https://example.com/image.jpg"}
    response = client.post("/enqueue", json=test_data)
    assert response.status_code == 201
    assert response.json() == {"message": "New task created."}
    method_frame, _, body = rabbit_connection.basic_get(TEST_QUEUE_NAME)
    assert method_frame is not None, "Message was not published to the queue"
    message = json.loads(body)
    assert message["img_url"] == test_data["img_url"]
