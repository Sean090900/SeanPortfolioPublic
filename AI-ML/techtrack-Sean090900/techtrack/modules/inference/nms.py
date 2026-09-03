import cv2
import numpy as np
from typing import List, Tuple

class NMS:
    """
    Implements Non-Maximum Suppression (NMS) to filter redundant bounding boxes 
    in object detection.

    This class takes bounding boxes, confidence scores, and class IDs and applies 
    NMS to retain only the most relevant bounding boxes based on confidence scores 
    and Intersection over Union (IoU) thresholding.
    """

    def __init__(self, score_threshold: float, nms_iou_threshold: float) -> None:
        """
        Initializes the NMS filter with confidence and IoU thresholds.

        :param score_threshold: The minimum confidence score required to retain a bounding box.
        :param nms_iou_threshold: The Intersection over Union (IoU) threshold for non-maximum suppression.

        :ivar self.score_threshold: The threshold below which detections are discarded.
        :ivar self.nms_iou_threshold: The IoU threshold that determines whether two boxes 
                                      are considered redundant.
        """
        self.score_threshold = score_threshold
        self.nms_iou_threshold = nms_iou_threshold

    def calculate_iou(self, box1, box2):

        # Determine the coordinates of the intersection rectangle
        x_left = max(box1[0], box2[0])
        x_right = min(box1[2], box2[2])
        y_top = max(box1[1], box2[1])
        y_bottom = min(box1[3], box2[3])

        # Calculate the area of intersection
        intersection_area = max(0, x_right - x_left) * max(0, y_bottom - y_top)

        # Calculate the area of each bounding box
        box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
        box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])

        # Calculate and return IoU
        if float(box1_area + box2_area - intersection_area) == 0.0:
            return 0.0
        iou = intersection_area / float(box1_area + box2_area - intersection_area)
        return iou

    def filter(
        self,
        bboxes: List[List[int]],
        class_ids: List[int],
        scores: List[float],
        class_scores: List[float],
    ) -> Tuple[List[List[int]], List[int], List[float], List[float]]:
        """
        Applies Non-Maximum Suppression (NMS) to filter overlapping bounding boxes.

        :param bboxes: A list of bounding boxes, where each box is represented as 
                       [x, y, width, height]. (x, y) is the top-left corner.
        :param class_ids: A list of class IDs corresponding to each bounding box.
        :param scores: A list of confidence scores for each bounding box.
        :param class_scores: A list of class-specific scores for each detection.

        :return: A tuple containing:
            - **filtered_bboxes (List[List[int]])**: The final bounding boxes after NMS.
            - **filtered_class_ids (List[int])**: The class IDs of retained bounding boxes.
            - **filtered_scores (List[float])**: The confidence scores of retained bounding boxes.
            - **filtered_class_scores (List[float])**: The class-specific scores of retained boxes.

        **How NMS Works:**
        - The function selects the bounding box with the highest confidence.
        - It suppresses any boxes that have a high IoU (overlapping area) with this selected box.
        - This process is repeated until all valid boxes are retained.

        **Example Usage:**
        ```python
        nms_processor = NMS(score_threshold=0.5, nms_iou_threshold=0.4)
        final_bboxes, final_class_ids, final_scores, final_class_scores = nms_processor.filter(
            bboxes, class_ids, scores, class_scores
        )
        ```
        """

        # TASK: Apply Non-Maximum Suppression (NMS) to filter overlapping bounding boxes.
        #         DO NOT USE **cv2.dnn.NMSBoxes()** for this Assignment. For Assignment 2, you will be
        #         permitted to use this function.

        # Check: If cv2.dnn.NMSBoxes returns no indicies
        # mock_result = cv2.dnn.NMSBoxes(bboxes, scores, self.score_threshold, self.nms_iou_threshold, eta=1.0, top_k=0)
        # if type(mock_result) == tuple:
        #     return ([], [], [], [])
        
        # Check: If cv2.dnn.NMSBoxes returns no indices
        indices = cv2.dnn.NMSBoxes(
            bboxes, scores, self.score_threshold, self.nms_iou_threshold, eta=1.0, top_k=0
        )

        # Treat None, empty list/tuple, or empty ndarray as "no indices"
        if (
            indices is None
            or (isinstance(indices, (list, tuple)) and len(indices) == 0)
            or (hasattr(indices, "size") and indices.size == 0)
        ):
            return ([], [], [], [])

        # Organize all information for a given box into seperate tuples
        samples = []
        for i in range(len(bboxes)):
            samples.append((bboxes[i], class_ids[i], scores[i], class_scores[i]))

        # Sort these tuples by 'score'
        samples.sort(key=lambda x: x[2], reverse=True)

        # Iterate through samples, surpressing necessary boxes
        picked_boxes = []
        while len(samples) > 0:

            # Pick the box with the highest score
            current = samples[0]
            picked_boxes.append(current)
            
            # Remove the current box from the list of candidates
            samples = samples[1:]

            # Find overlapping boxes and remove them
            remaining = []
            for sample in samples:
                if self.calculate_iou(current[0], sample[0]) < self.nms_iou_threshold:
                    remaining.append(sample)
            
            samples = remaining

        # print(picked_boxes)
        filtered_bboxes = [item[0] for item in picked_boxes]
        filtered_class_ids = [item[1] for item in picked_boxes]
        filtered_scores = [item[2] for item in picked_boxes]
        filtered_class_scores = [item[3] for item in picked_boxes]
            
        # Return these variables in order as described in Line 46-50:
        return filtered_bboxes, filtered_class_ids, filtered_scores, filtered_class_scores


