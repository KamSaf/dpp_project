import os
from pathlib import Path


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
ROOT = Path(__file__).parent.parent
RABBIT_HOST = os.getenv("RABBIT_HOST", "localhost")
QUEUE_NAME = os.getenv("QUEUE_NAME", "img_queue")
