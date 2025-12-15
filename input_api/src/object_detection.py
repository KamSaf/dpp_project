import cv2
import numpy as np
import imutils


def process_img(image: cv2.typing.MatLike) -> int:
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())  # type: ignore
    MAX_WIDTH = 1500
    if image.shape[0] > MAX_WIDTH:
        ratio = image.shape[0] / MAX_WIDTH
        image = imutils.resize(image, width=MAX_WIDTH, height=image.shape[1] * ratio)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    regions, weights = hog.detectMultiScale(
        gray, winStride=(2, 2), padding=(5, 5), scale=1.02
    )
    mean = np.mean(weights)
    std = np.std(weights)
    k = 0.86
    filtered_objects = []
    for index, weight in enumerate(weights):
        if weight >= (mean - k * std):
            filtered_objects.append(regions[index])
    for object in filtered_objects:
        x, y, w, h = object
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return len(filtered_objects)
