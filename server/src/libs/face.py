import cv2
import mediapipe as mp
import numpy as np


class FaceDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

    def predict(self, image):
        # Detect faces in the image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5
        )
        return faces  # Return detected faces


class FaceLandmarksDetector:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(max_num_faces=1)

    def estimate_gaze(self, image: np.ndarray):
        """
        Estimate gaze direction using MediaPipe Face Mesh.

        Args:
            image (numpy.ndarray): Input image (BGR format).

        Returns:
            dict: Gaze coordinates in normalized form {'x': float, 'y': float}.
        """
        # Convert the image to RGB and process it with Face Mesh
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(image_rgb)

        if results.multi_face_landmarks:
            # Get the first face's landmarks
            landmarks = results.multi_face_landmarks[0].landmark

            # Extract left and right eye landmarks using MediaPipe constants
            left_eye_indices = set(sum(self.mp_face_mesh.FACEMESH_LEFT_EYE, ()))
            right_eye_indices = set(sum(self.mp_face_mesh.FACEMESH_RIGHT_EYE, ()))

            left_eye_landmarks = np.array(
                [(landmarks[idx].x, landmarks[idx].y) for idx in left_eye_indices]
            )
            right_eye_landmarks = np.array(
                [(landmarks[idx].x, landmarks[idx].y) for idx in right_eye_indices]
            )

            # Calculate the center of each eye
            left_eye_center = np.mean(left_eye_landmarks, axis=0)
            right_eye_center = np.mean(right_eye_landmarks, axis=0)

            # Estimate the pupil position (simplified approximation)
            left_pupil = np.mean(
                left_eye_landmarks[
                    [
                        list(left_eye_indices).index(159),
                        list(left_eye_indices).index(160),
                    ]
                ],
                axis=0,
            )
            right_pupil = np.mean(
                right_eye_landmarks[
                    [
                        list(right_eye_indices).index(386),
                        list(right_eye_indices).index(387),
                    ]
                ],
                axis=0,
            )

            # Calculate gaze direction (relative to the eye center)
            left_gaze = left_pupil - left_eye_center
            right_gaze = right_pupil - right_eye_center

            # Normalize the gaze direction
            left_gaze_normalized = left_gaze / np.linalg.norm(left_gaze)
            right_gaze_normalized = right_gaze / np.linalg.norm(right_gaze)

            # Average the gaze directions of both eyes
            gaze_x = (left_gaze_normalized[0] + right_gaze_normalized[0]) / 2.0
            gaze_y = (left_gaze_normalized[1] + right_gaze_normalized[1]) / 2.0

            return {"x": gaze_x, "y": -gaze_y}  # Flip y-axis for screen coordinates

        return {"x": 0.5, "y": 0.5}  # Default fallback if no face is detected

    # def visualize(self, image, detections):
    #     # Implement visualization logic here
    #     for landmarks in detections:
    #         for landmark in landmarks.landmark:
    #             h, w, _ = image.shape
    #             x, y = int(landmark.x * w), int(landmark.y * h)
    #             cv2.circle(image, (x, y), 1, (0, 255, 0), -1)  # Draw landmarks
    #     return image

    def draw_gaze(image, gaze_coordinates):
        """
        Draw the gaze direction on the image.

        Args:
            image (numpy.ndarray): Input image (BGR format).
            gaze_coordinates (dict): Gaze coordinates {'x': float, 'y': float}.

        Returns:
            numpy.ndarray: Image with gaze direction drawn.
        """
        h, w, _ = image.shape
        gaze_x, gaze_y = gaze_coordinates["x"], gaze_coordinates["y"]

        # Scale gaze coordinates to image dimensions
        gaze_point = (int(gaze_x * w), int(gaze_y * h))

        # Draw a circle at the gaze point
        cv2.circle(image, gaze_point, 10, (0, 255, 0), -1)

        return image
