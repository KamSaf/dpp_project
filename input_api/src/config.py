import os
from pathlib import Path


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
ROOT = Path(__file__).parent.parent
RABBIT_HOST = os.getenv("RABBIT_HOST", "localhost")
QUEUE_NAME = os.getenv("QUEUE_NAME", "img_queue")
DB_API_HOST = os.getenv("DB_API_HOST", "db_api")
DB_API_PORT = os.getenv("DB_API_PORT", "3000")
