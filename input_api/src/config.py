import os
from pathlib import Path


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
ROOT = Path(__file__).parent.parent
RABBIT_HOST = os.getenv("rabbitmq")
QUEUE_NAME = os.getenv("img_queue")
