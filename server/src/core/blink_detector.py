import cv2
import numpy as np
from scipy.spatial import distance as dist


def eye_aspect_ratio(eye: list[float]) -> float:
    """Compute the eye aspect ratio (EAR) for a given set of eye landmarks."""
    # Calculate the distances between vertical eye landmarks
    A = dist.euclidean(eye[1], eye[5])  # Distance between top and bottom of the eye
    B = dist.euclidean(eye[2], eye[4])  # Distance between second pair of top and bottom

    # Calculate the distance between horizontal eye landmarks
    C = dist.euclidean(eye[0], eye[3])  # Distance between left and right of the eye

    # Compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)
    return ear


def detect_blinks(
    image: np.ndarray,
    face_cascade: cv2.CascadeClassifier,
    eye_cascade: cv2.CascadeClassifier,
    ear_threshold: float = 0.2,
    consecutive_frames: int = 2,
) -> str:
    """
    Detect blinks in the given image using the Eye Aspect Ratio (EAR).
    """
    # Convert the image to grayscale for face and eye detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
    )

    # Initialize variables for blink detection
    blink_detected = False
    frame_counter = 0

    for x, y, w, h in faces:
        # Extract the region of interest (ROI) for the face
        roi_gray = gray[y : y + h, x : x + w]

        # Detect eyes in the ROI
        eyes = eye_cascade.detectMultiScale(roi_gray)

        # Ensure both eyes are detected
        if len(eyes) == 2:
            # Extract the first two detected eyes (left and right)
            left_eye, right_eye = eyes[:2]

            # Define the eye landmarks (simplified for demonstration)
            # In a real-world scenario, you'd use a facial landmark detector like dlib or MediaPipe
            left_eye_points = [
                (left_eye[0], left_eye[1]),  # Top-left corner
                (left_eye[0] + left_eye[2] // 4, left_eye[1]),  # Mid-top
                (left_eye[0] + left_eye[2] // 2, left_eye[1]),  # Right-top
                (
                    left_eye[0] + left_eye[2],
                    left_eye[1] + left_eye[3] // 2,
                ),  # Right-center
                (
                    left_eye[0] + left_eye[2] // 2,
                    left_eye[1] + left_eye[3],
                ),  # Right-bottom
                (
                    left_eye[0] + left_eye[2] // 4,
                    left_eye[1] + left_eye[3],
                ),  # Mid-bottom
            ]

            right_eye_points = [
                (right_eye[0], right_eye[1]),  # Top-left corner
                (right_eye[0] + right_eye[2] // 4, right_eye[1]),  # Mid-top
                (right_eye[0] + right_eye[2] // 2, right_eye[1]),  # Right-top
                (
                    right_eye[0] + right_eye[2],
                    right_eye[1] + right_eye[3] // 2,
                ),  # Right-center
                (
                    right_eye[0] + right_eye[2] // 2,
                    right_eye[1] + right_eye[3],
                ),  # Right-bottom
                (
                    right_eye[0] + right_eye[2] // 4,
                    right_eye[1] + right_eye[3],
                ),  # Mid-bottom
            ]

            # Compute the EAR for both eyes
            left_ear = eye_aspect_ratio(left_eye_points)
            right_ear = eye_aspect_ratio(right_eye_points)

            # Average the EAR for both eyes
            ear = (left_ear + right_ear) / 2.0

            # Check if the EAR is below the threshold
            if ear < ear_threshold:
                frame_counter += 1
                # If the eye has been below the threshold for enough consecutive frames, detect a blink
                if frame_counter >= consecutive_frames:
                    blink_detected = True
            else:
                frame_counter = (
                    0  # Reset the frame counter if EAR is above the threshold
                )

    # Return the result
    return "Blink Detected" if blink_detected else None
