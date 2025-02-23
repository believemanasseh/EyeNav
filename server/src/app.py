import cv2
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from src.core.blink_detector import detect_blinks
from src.utils.helpers import process_image

app = FastAPI(docs_url="/")

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")


@app.get("/home")
def read_root():
    return {"Hello": "World"}


@app.websocket("/ws")
async def connect(websocket: WebSocket):
    try:
        await websocket.accept()
        while True:
            data = await websocket.receive_text()
            scroll_direction, image, coordinates = process_image(data)
            blink_status = detect_blinks(image, face_cascade, eye_cascade)
            response = {
                "scrollDirection": scroll_direction,
                "blinkStatus": blink_status,
                "coordinates": coordinates,
            }
            await websocket.send_json(response)
    except WebSocketDisconnect:
        print("WebSocket disconnected!")
    except Exception as e:
        print(f"Error: {e}")
