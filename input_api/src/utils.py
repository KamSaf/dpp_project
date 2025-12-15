import numpy as np
import requests
import cv2


def load_image_from_url(url: str) -> cv2.typing.MatLike | None:
    response = requests.head(url)
    content_type = response.headers.get("Content-Type")
    if not content_type or not content_type.startswith("image/"):
        return None
    try:
        img_data = requests.get(url).content
        img_array = np.frombuffer(img_data, dtype=np.uint8)
        return cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    except Exception:
        raise ValueError("Invalid data provided.")
