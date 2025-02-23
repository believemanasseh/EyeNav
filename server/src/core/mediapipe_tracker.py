import cv2

from .gaze_interpreter import interpret_gaze  # Import the gaze interpreter
from .iris_detector import IrisDetector


class GazeTracker:
    def __init__(self):
        self.iris_detector = IrisDetector()

    def track_gaze(self, image: cv2.typing.MatLike):
        left_eye_image, right_eye_image = self.iris_detector.preprocess(image)

        left_eye_iris, left_eye_contour = self.iris_detector.predict(left_eye_image)
        right_eye_iris, right_eye_contour = self.iris_detector.predict(
            right_eye_image, isLeft=False
        )

        # Interpret gaze coordinates
        interpreted_result = interpret_gaze(left_eye_iris, right_eye_iris)

        return {
            "left_iris": (left_eye_iris[0], left_eye_iris[1]),
            "right_iris": (right_eye_iris[0], right_eye_iris[1]),
            "interpreted_result": interpreted_result,
        }
