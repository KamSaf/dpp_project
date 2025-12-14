import time
import requests
from src.config import ROOT


def save_image_from_url(url: str) -> str | None:
    response = requests.head(url)
    content_type = response.headers.get("Content-Type")
    if content_type and content_type.startswith("image/"):
        ext = content_type.split("/")[-1]
    else:
        return None
    try:
        img_data = requests.get(url).content
    except Exception:
        return None
    file_name = f"{str(time.time()).replace('.', '')}.{ext}"
    file_path = f"{ROOT}/images/{file_name}"
    with open(file_path, "wb") as handler:
        handler.write(img_data)
    return file_name
