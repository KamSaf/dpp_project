import os
from fastapi.testclient import TestClient
from src.main import app
from dotenv import load_dotenv

load_dotenv()


client = TestClient(app)

TEST_RABBIT_HOST = os.getenv("TEST_RABBIT_HOST", "test-rabbitmq")
TEST_QUEUE_NAME = os.getenv("TEST_QUEUE_NAME", "img_queue")
