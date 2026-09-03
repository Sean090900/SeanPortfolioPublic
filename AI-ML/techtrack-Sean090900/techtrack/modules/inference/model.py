import cv2
import numpy as np
from typing import List, Tuple


class Detector:
    """
    A class that represents an object detection model using OpenCV's DNN module
    with a YOLO-based architecture.
    """

    def __init__(self, weights_path: str, config_path: str, class_path: str, score_threshold: float=.5) -> None:
        """
        Initializes the YOLO model by loading the pre-trained network and class labels.

        :param weights_path: Path to the pre-trained YOLO weights file.
        :param config_path: Path to the YOLO configuration file.
        :param class_path: Path to the file containing class labels.

        :ivar self.net: The neural network model loaded from weights and config files.
        :ivar self.classes: A list of class labels loaded from the class_path file.
        :ivar self.img_height: Height of the input image/frame.
        :ivar self.img_width: Width of the input image/frame.
        """
        self.net = cv2.dnn.readNet(weights_path, config_path)

        # Load class labels
        with open(class_path, "r") as f:
            self.classes = [line.strip() for line in f.readlines()]

        self.img_height: int = 0
        self.img_width: int = 0

        self.score_threshold = score_threshold

    def predict(self, preprocessed_frame: np.ndarray) -> List[np.ndarray]:
        """
        Runs the YOLO model on a single input frame and returns raw predictions.

        :param preprocessed_frame: A single image frame that has been preprocessed 
                                   for YOLO model inference (e.g., resized and normalized).

        :return: A list of NumPy arrays containing the raw output from the YOLO model.
                 Each output consists of multiple detections with bounding boxes, 
                 confidence scores, and class probabilities.

        :ivar self.img_height: The height of the input image/frame.
        :ivar self.img_width: The width of the input image/frame.

        **YOLO Output Format:**
        Each detection in the output contains:
        - First 4 values: Bounding box center x, center y, width, height.
        - 5th value: Confidence score.
        - Remaining values: Class probabilities for each detected object.

        **Reference:**
        - OpenCV YOLO Documentation: 
          https://opencv-tutorial.readthedocs.io/en/latest/yolo/yolo.html#create-a-blob
        """
        self.img_height, self.img_width = preprocessed_frame.shape[:2]

        # TASK: Use the YOLO model to return all raw outputs
        layer_names = self.net.getLayerNames()
        output_layers = [layer_names[i-1] for i in self.net.getUnconnectedOutLayers()]

        blob = cv2.dnn.blobFromImage(
            preprocessed_frame,
            scalefactor=1/255.,
            size=(416, 416),
            mean=(0, 0, 0),
            swapRB=True,
            crop=False
        )

        self.net.setInput(blob)
        
        # Return model outputs
        outputs = self.net.forward(output_layers)
        return outputs

    def post_process(
        self, predict_output: List[np.ndarray]
    ) -> Tuple[List[List[int]], List[int], List[float], List[np.ndarray]]:
        """
        Processes the raw YOLO model predictions and filters out low-confidence detections.

        :param predict_output: A list of NumPy arrays containing raw predictions 
                               from the YOLO model.

        :return: A tuple containing:
            - **bboxes (List[List[int]])**: List of bounding boxes as `[x, y, width, height]`, 
              where (x, y) represents the top-left corner.
            - **class_ids (List[int])**: List of detected object class indices.
            - **confidence_scores (List[float])**: List of confidence scores for each detection.
            - **class_scores (List[np.ndarray])**: List of all class-specific confidence scores.

        **Post-processing steps:**
        1. Extract bounding box coordinates from YOLO output.
        2. Compute class probabilities and determine the most likely class.
        3. Filter out detections below the confidence threshold.
        4. Convert bounding box coordinates from center-based format to 
           top-left corner format.

        **Bounding Box Conversion:**
        YOLO outputs bounding box coordinates in the format:
        ```
        center_x, center_y, width, height
        ```
        This function converts them to:
        ```
        x, y, width, height
        ```
        where (x, y) is the top-left corner.

        **Reference:**
        - OpenCV YOLO Documentation: 
          https://opencv-tutorial.readthedocs.io/en/latest/yolo/yolo.html#create-a-blob
        """
        
        # TASK: Use the YOLO model to return list of NumPy arrays filtered
        #         by processing the raw YOLO model predictions and filters out 
        #         low-confidence detections (i.e., < score_threshold). Use the logic
        #         in Line 83-88.

        bboxes = []
        class_ids = []
        confidence_scores = []
        class_scores_list = []

        for feature_maps in predict_output:
            for detection in feature_maps:
                if detection[4] > self.score_threshold:

                    # Convert box coordinates
                    x_center_raw = detection[0] * self.img_width
                    y_center_raw = detection[1] * self.img_height
                    width_raw = int(detection[2] * self.img_width)
                    height_raw = int(detection[3] * self.img_height)
                    x_left = int(x_center_raw - (width_raw / 2))
                    y_top = int(y_center_raw - (height_raw / 2))

                    # Convert bounding box values for format: [x, y, width, height]
                    bboxes.append([x_left, y_top, width_raw, height_raw])
                    confidence_scores.append(detection[4])
                    class_scores_list.append(detection[5:])
                    class_ids.append(np.argmax(detection[5:]))

        # Return these variables in order:
        return bboxes, class_ids, confidence_scores, class_scores_list


"""
EXAMPLE USAGE:
model = Detector()

# Perform object detection on the current frame
predictions = self.detector.predict(frame)

# Extract bounding boxes, class IDs, confidence scores, and class-specific scores
bboxes, class_ids, confidence_scores, class_scores = self.detector.post_process(
    predictions
)
"""
# import tempfile

# # Create a temporary file for class labels.
# temp_class_file = tempfile.NamedTemporaryFile(delete=False, mode="w+t")
# classes = [
#     "barcode", "car", "cardboard box", "fire", "forklift", "freight container",
#     "gloves", "helmet", "ladder", "license plate", "person", "qr code", "road sign",
#     "safety vest", "smoke", "traffic cone", "traffic light", "truck", "van", "wood pallet"
# ]
# temp_class_file.write("\n".join(classes))
# temp_class_file.flush()
# temp_class_file.close()
# # weights_path = from_project_root("techtrack", "storage", "yolo_model_1", "yolov4-tiny-logistics_size_416_1.weights")
# # cfg_path = from_project_root("techtrack", "storage", "yolo_model_1", "yolov4-tiny-logistics_size_416_1.cfg")
# weights_path = '/Users/seandickson/JohnsHopkinsScripts/CreatingAIEnabledSystems/techtrack-Sean090900/techtrack/storage/yolo_model_1/yolov4-tiny-logistics_size_416_1.weights'
# cfg_path = '/Users/seandickson/JohnsHopkinsScripts/CreatingAIEnabledSystems/techtrack-Sean090900/techtrack/storage/yolo_model_1/yolov4-tiny-logistics_size_416_1.cfg'

# detector = Detector(weights_path, cfg_path, temp_class_file.name, score_threshold=0.5)
# detector.img_width = 400
# detector.img_height = 300

# detection1 = np.array([0.5, 0.5, 0.2, 0.2, 0.9, 0.1, 0.8, 0.05])
# detection2 = np.array([0.3, 0.3, 0.1, 0.1, 0.1, 0.2, 0.1, 0.3])
# predict_output = [np.array([detection1, detection2])]

# bboxes, class_ids, confidence_scores, class_scores = detector.post_process(predict_output)

# print(class_scores)
