import itertools
import numpy as np

class Loss:
    """
    *Modified* YOLO Loss for Hard Negative Mining.

    Attributes:
        num_classes (int): Number of classes.
        iou_threshold (float): Intersection over Union (IoU) threshold.
        lambda_coord (float): Weighting factor for localization loss.
        lambda_noobj (float): Weighting factor for no object confidence loss.
    """

    def __init__(self, iou_threshold=0.5, lambda_coord=0.5, lambda_obj=0.5, lambda_noobj=0.5, lambda_cls=0.5, num_classes=20):
        """
        Initialize the Loss object with the given parameters.

        Internal Process:
        1. Stores the provided hyperparameters as instance attributes.
        2. Defines the column names for loss components to track them in results.

        Args:
            num_classes (int): Number of classes.
            lambda_coord (float): Weighting factor for localization loss.
            lambda_obj (float): Weighting factor for objectness loss.
            lambda_noobj (float): Weighting factor for no object confidence loss.
            lambda_cls (float): Weighting factor for classification loss.
        """
        self.num_classes = num_classes
        self.lambda_coord = lambda_coord
        self.lambda_cls = lambda_cls
        self.lambda_obj = lambda_obj
        self.lambda_noobj = lambda_noobj
        self.columns = [
            'total_loss', 
            'loc_loss', 
            'conf_loss_obj', 
            'conf_loss_noobj', 
            'class_loss'
        ]
        self.iou_threshold = iou_threshold

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
        iou = intersection_area / float(box1_area + box2_area - intersection_area)
        return iou
    
    def get_predictions(self, predictions):
        """
        Extracts bounding box coordinates, objectness scores, and class scores from predictions.

        Internal Process:
        1. Iterates over predictions to extract bounding box coordinates.
        2. Extracts objectness scores.
        3. Extracts class scores.

        Args:
            predictions (list): List of predicted bounding boxes and associated scores.
        
        Returns:
            tuple: (bounding boxes, objectness scores, class scores)
        """
        pred_box = []
        objectness_score = []
        class_scores = []
        for prediction in predictions:
            for feature_map in prediction:
                pred_box.append(feature_map[:4])
                objectness_score.append(feature_map[4])
                class_scores.append(feature_map[5:])
        return np.array(pred_box), np.array(objectness_score), np.array(class_scores)
    
    def get_annotations(self, annotations):
        """
        Extract ground truth bounding boxes and class IDs from annotations.
        
        Internal Process:
        1. Iterates over annotations to extract bounding box coordinates.
        2. Extracts the corresponding class labels.
        
        Args:
            annotations (list): List of ground truth annotations.
        
        Returns:
            tuple: (ground truth bounding boxes, class labels)
        """
        gt_boxes = []
        gt_class_ids = []
        for annotation in annotations:
            gt_boxes.append(annotation[1:])
            gt_class_ids.append(annotation[0])
        return np.array(gt_boxes), np.array(gt_class_ids)
    
    def compute(self, predictions, annotations):
        """
        Compute the YOLO loss components.

        Internal Process:
        1. Extracts predictions and annotations of a single image/frame.
        2. Iterates through annotations to compute localization, confidence, and class loss.
        3. Computes total loss using predefined weighting factors.

        Args:
            predictions (list): List of predictions of a single image.
            annotations (list): List of ground truth annotations of a single image.

        Returns:
            dict: Dictionary containing the computed loss components.
        """
        # TASK: Complete this method to compute the Loss function.
        #         This method calculates the localization, objectness 
        #         (or confidence) and classification loss.
        #         This method will be called in the HardNegativeMiner class.
        #         ----------------------------------------------------------
        #         HINT: For simplicity complete use get_predictions(), get_annotations().
        #         You may add class methods to improve the readability of this code. 

        eps = 1e-9

        # ---- Extract predictions & targets ----
        pred_boxes, obj_scores, class_scores = self.get_predictions(predictions)
        gt_boxes, gt_cls = self.get_annotations(annotations)

        N = pred_boxes.shape[0] if pred_boxes.size else 0
        M = gt_boxes.shape[0] if gt_boxes.size else 0

        # Trivial zero case
        if N == 0 and M == 0:
            return {'total_loss': 0.0, 'loc_loss': 0.0, 'conf_loss_obj': 0.0, 'conf_loss_noobj': 0.0, 'class_loss': 0.0}

        # Stable softmax
        def softmax(x):
            x = x - np.max(x, axis=-1, keepdims=True)
            ex = np.exp(x)
            return ex / (np.sum(ex, axis=-1, keepdims=True) + eps)

        # ---- IoU matrix (N x M) ----
        if M > 0 and N > 0:
            iou_mat = np.zeros((N, M), dtype=float)
            for i in range(N):
                for j in range(M):
                    iou_mat[i, j] = self.calculate_iou(pred_boxes[i], gt_boxes[j])

            # ---- Greedy one-to-one matching (fix: no broadcasting tricks) ----
            matched_pred = []
            matched_gt = []
            used_pred = set()

            for j in range(M):
                # ignore already-used preds by temporarily setting their IoU to -1 for this column
                col = iou_mat[:, j].copy()
                if used_pred:
                    # make a boolean mask of unused preds
                    mask_unused = np.ones(N, dtype=bool)
                    mask_unused[list(used_pred)] = False
                    # among unused only, take argmax
                    if np.any(mask_unused):
                        cand_idx = np.argmax(col[mask_unused])
                        # map back to absolute index
                        abs_idx = np.flatnonzero(mask_unused)[cand_idx]
                        best_i, best_iou = abs_idx, col[abs_idx]
                    else:
                        best_i, best_iou = -1, -1.0
                else:
                    best_i = int(np.argmax(col))
                    best_iou = col[best_i]

                if best_i != -1 and best_iou >= self.iou_threshold:
                    matched_pred.append(best_i)
                    matched_gt.append(j)
                    used_pred.add(best_i)

            matched_pred = np.array(matched_pred, dtype=int) if matched_pred else np.array([], dtype=int)
            matched_gt   = np.array(matched_gt,   dtype=int) if matched_gt   else np.array([], dtype=int)
        else:
            matched_pred = np.array([], dtype=int)
            matched_gt   = np.array([], dtype=int)

        # ---- Positives / Negatives ----
        pos_idx = matched_pred
        all_idx = np.arange(N, dtype=int) if N > 0 else np.array([], dtype=int)
        neg_idx = np.setdiff1d(all_idx, pos_idx, assume_unique=False)

        # ---- Localization loss (positives only) ----
        if pos_idx.size > 0:
            pred_loc = pred_boxes[pos_idx]            # (P,4)
            gt_loc   = gt_boxes[matched_gt]           # (P,4)
            loc_loss = float(np.mean(np.sum((pred_loc - gt_loc) ** 2, axis=1)))
        else:
            loc_loss = 0.0

        # ---- Objectness losses (BCE) ----
        if N > 0:
            p_obj = np.clip(obj_scores.astype(float), eps, 1.0 - eps)
        else:
            p_obj = np.array([], dtype=float)

        conf_loss_obj = float(-np.mean(np.log(p_obj[pos_idx] + eps))) if pos_idx.size > 0 else 0.0
        conf_loss_noobj = float(-np.mean(np.log(1.0 - p_obj[neg_idx] + eps))) if neg_idx.size > 0 else 0.0

        # ---- Classification loss (positives only) ----
        if pos_idx.size > 0:
            cls_slice = class_scores[pos_idx]  # (P, C')
            probs = softmax(cls_slice)
            C_eff = probs.shape[1]
            tgt = gt_cls[matched_gt].astype(int).reshape(-1)  # ensure shape (P,)
            tgt = np.clip(tgt, 0, C_eff - 1)
            class_loss = float(-np.mean(np.log(probs[np.arange(probs.shape[0]), tgt] + eps)))
        else:
            class_loss = 0.0

        # ---- Weighted total ----
        total_loss = (
            self.lambda_coord * loc_loss
            + self.lambda_obj   * conf_loss_obj
            + self.lambda_noobj * conf_loss_noobj
            + self.lambda_cls   * class_loss
        )

        return {
            'total_loss': float(total_loss),
            'loc_loss': float(loc_loss),
            'conf_loss_obj': float(conf_loss_obj),
            'conf_loss_noobj': float(conf_loss_noobj),
            'class_loss': float(class_loss),
        }

        # # Convert to arrays for safety (still iterate elementwise)
        # preds = predictions
        # gts = annotations

        # # Loss scalars
        # loc_loss = 0.0              # localization loss
        # class_loss = 0.0            # classification loss (cross-entropy on class logits)
        # conf_loss_obj = 0.0         # object confidence loss
        # conf_loss_noobj = 0.0       # no-object confidence loss

        # # Standard YOLO-style weights
        # lambda_coord = 5.0
        # lambda_noobj = 0.5
        # eps = 1e-9

        # # Pair predictions with annotations one-to-one by index
        # # (If you need matching by IoU/greedy assignment, that’s a larger change; this keeps to the docstring’s simple loop.)
        # n = min(len(preds), len(gts))
        # for i in range(n):
        #     p = np.asarray(preds[i], dtype=float)
        #     g = np.asarray(gts[i], dtype=float)

        #     # Unpack
        #     px, py, pw, ph, p_conf = p[i][:5]
        #     p_logits = p[i][5:]  # class logits (not probabilities)

        #     g_cls, gx, gy, gw, gh = g[:5]
        #     g_cls = int(g_cls)

        #     # 1) Localization loss (SSE on (x,y) and log-space on (w,h))
        #     loc_xy = (px - gx) ** 2 + (py - gy) ** 2
        #     loc_wh = (np.log(pw + eps) - np.log(gw + eps)) ** 2 + (np.log(ph + eps) - np.log(gh + eps)) ** 2
        #     loc_loss += loc_xy + loc_wh

        #     # 2) Confidence losses
        #     iou = self.calculate_iou((px, py, pw, ph), (gx, gy, gw, gh))
        #     conf_loss_obj += (p_conf - iou) ** 2
        #     conf_loss_noobj += (p_conf - 0.0) ** 2

        #     # 3) Classification loss (cross-entropy on logits)
        #     if p_logits.size > 0:
        #         # softmax then NLL for the true class
        #         # Numerically stable softmax
        #         maxlog = np.max(p_logits)
        #         exps = np.exp(p_logits - maxlog)
        #         probs = exps / (np.sum(exps) + eps)
        #         # Cross-entropy for the true class
        #         # Clip for safety then compute -log(p_true)
        #         p_true = np.clip(probs[g_cls], eps, 1.0)
        #         class_loss += -np.log(p_true)
        #     else:
        #         # If no class scores are present, contribute nothing
        #         class_loss += 0.0

        # total_loss = lambda_coord * loc_loss + class_loss + conf_loss_obj + lambda_noobj * conf_loss_noobj

        # return {
        #     "loc_loss": float(loc_loss),
        #     "class_loss": float(class_loss),
        #     "conf_loss_obj": float(conf_loss_obj),
        #     "conf_loss_noobj": float(conf_loss_noobj),
        #     "total_loss": float(total_loss),
        # }

# loss = Loss(iou_threshold=0.5, lambda_coord=0.5, lambda_noobj=0.5, num_classes=3)
# predictions = [
#     [[10, 10, 20, 20, 0.9, 0.8, 0.1, 0.1]]
# ]
# annotations = [
#     [0, 10, 10, 20, 20]
# ]
# losses = loss.compute(predictions, annotations)

# for key in losses:
#     print(key, losses[key])


