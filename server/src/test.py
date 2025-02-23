import base64
from io import BytesIO

import cv2
import mediapipe as mp
import numpy as np
import requests
import torch
from PIL import Image
from transformers import LlavaNextForConditionalGeneration, LlavaNextProcessor

model_path = "ibm-granite/granite-vision-3.1-2b-preview"
processor = LlavaNextProcessor.from_pretrained(model_path)

model = LlavaNextForConditionalGeneration.from_pretrained(model_path).to(
    "cuda" if torch.cuda.is_available() else "cpu"
)


def url_to_base64(image_url):
    try:
        # Fetch the image from the URL
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Read the image content
        image_data = response.content

        # Optionally, you can open and verify the image using PIL
        # This step is optional but ensures the fetched data is a valid image
        Image.open(
            BytesIO(image_data)
        )  # This will raise an error if the image is invalid

        # Encode the image data as base64
        base64_encoded = base64.b64encode(image_data).decode("utf-8")

        return base64_encoded

    except Exception as e:
        print(f"Error converting image to base64: {e}")
        return None


class FaceLandmarksDetector:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1, refine_landmarks=True
        )

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
            print(landmarks, len(landmarks), "lsld")

            # Extract left and right eye landmarks using MediaPipe constants
            left_eye_indices = set(sum(self.mp_face_mesh.FACEMESH_LEFT_EYE, ()))
            right_eye_indices = set(sum(self.mp_face_mesh.FACEMESH_RIGHT_EYE, ()))
            print(left_eye_indices, right_eye_indices, "inr")

            # Extract iris landmarks
            left_iris_indices = set(sum(self.mp_face_mesh.FACEMESH_LEFT_IRIS, ()))
            right_iris_indices = set(sum(self.mp_face_mesh.FACEMESH_RIGHT_IRIS, ()))
            print(left_iris_indices, right_iris_indices, "ir")

            # Collect landmarks for eyes and irises
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
                        list(left_eye_indices).index(386),
                        list(left_eye_indices).index(387),
                    ]
                ],
                axis=0,
            )
            right_pupil = np.mean(
                right_eye_landmarks[
                    [
                        list(right_eye_indices).index(159),
                        list(right_eye_indices).index(160),
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


def interpret_gaze(coordinates: dict[str, float]):
    """
    Interprets gaze data using IBM Granite Vision Model.
    """
    print(coordinates, "cooslds")

    system_prompt = "System Prompt: You are to determine the user intent given the gaze coordinates (x, y). Intents include scrolling up or down. Keep answer as precise as possible (e.g. 'up' or 'down')"

    user_prompt = f"User Prompt: Gaze coordinates: x=({coordinates['x']})), y=({coordinates['y']}). Interpret the user's intent."

    conversation = [
        {"role": "system", "content": [{"type": "text", "text": system_prompt}]},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": user_prompt},
            ],
        },
    ]
    inputs = processor.apply_chat_template(
        conversation,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
    ).to("cuda")

    # autoregressively complete prompt
    output = model.generate(**inputs, max_new_tokens=100)

    response = processor.decode(output[0], skip_special_tokens=True)
    print(response)
    return response


def decode_base64_to_ndarray(base64_string: str) -> cv2.typing.MatLike:
    """Decode base64 string to OpenCV image."""
    if base64_string.startswith("data:image/jpeg;base64,"):
        base64_string = base64_string.split(",")[1]
    image_bytes = base64.b64decode(base64_string)
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image


def process_image(base64_string: str):
    """Process the image to detect gaze."""
    try:
        print(base64_string, "sd")
        gaze_estimator = FaceLandmarksDetector()
        image = decode_base64_to_ndarray(base64_string)
        print(image, "img")
        coordinates = gaze_estimator.estimate_gaze(image)
        print(coordinates, "here ??")
        interpretation = interpret_gaze(coordinates)
        print(interpretation, "inter???")
        return interpretation
    except Exception as e:
        print(f"Error processing image: {e}")
        return None


def inference():
    image = url_to_base64(
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTYVRc6YylXrO1M4zC4J0ipsfOCJ7TzGZiVaQ&s"
    )
    process_image(image)


if __name__ == "__main__":
    inference()
