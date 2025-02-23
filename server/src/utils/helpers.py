import base64

import cv2
import numpy as np

from src.core.gaze_interpreter import interpret_gaze
from src.libs.face import FaceLandmarksDetector

gaze_estimator = FaceLandmarksDetector()


def decode_base64_to_ndarray(base64_string: str) -> cv2.typing.MatLike:
    """Decode base64 string to OpenCV image."""
    if base64_string.startswith("data:image/jpeg;base64,"):
        base64_string = base64_string.split(",")[1]
    image_bytes = base64.b64decode(base64_string)
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image


def ndarray_to_base64(image, quality=90):
    """Convert an ndarray image to a base64-encoded string."""
    _, buffer = cv2.imencode(".jpg", image, [cv2.IMWRITE_JPEG_QUALITY, quality])
    return base64.b64encode(buffer).decode("utf-8")


def process_image(
    base64_string: str,
) -> tuple[str, np.ndarray, dict[str, float]] | None:
    """Process the image to detect gaze."""
    try:
        image = decode_base64_to_ndarray(base64_string)
        coordinates = gaze_estimator.estimate_gaze(image)
        scroll_direction = interpret_gaze(coordinates)
        return scroll_direction, image, coordinates
    except Exception as e:
        print(f"Error processing image: {e}")
        return None


def format_gaze_data(coordinates):
    if coordinates:
        return f"Left Iris: {coordinates['left_iris']}, Right Iris: {coordinates['right_iris']}"
    return "No gaze data available."
