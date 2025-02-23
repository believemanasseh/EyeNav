import logging

def setup_logger():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_gaze_data(coordinates):
    if coordinates:
        logging.info(f"Left Iris Coordinates: {coordinates['left_iris']}")
        logging.info(f"Right Iris Coordinates: {coordinates['right_iris']}")
    else:
        logging.warning("No gaze data received.")
