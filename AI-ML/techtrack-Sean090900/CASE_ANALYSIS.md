## Case Study Analysis | TechTrack - Object Detection

Sean Dickson

*Date: 10/8/25*


### 1. Model Performance Comparison (Model Selection):

**Objective: Compare YOLO models 1 and 2 and compare relative Mean-Average Precision metrics across all classes.**

|Metric   |Model 1  |Model 2  |
|---------|---------|---------|
|mAP      |0.4557   |0.4722   |

*Table 1: Comparing Mean-Average Precision (mAP) between YOLO models*

Model 1 Precision-Recall Curves:

[Model 1 Recall Curves](techtrack/analysis/model1_curves)

Model 2 Precision-Recall Curve:

[Model 2 Recall Curves](techtrack/analysis/model2_curves)

Both YOLO models provided object predictions at roughly the same Mean-Average Precision, with model 2 showing only a slightly better performance. 

In terms of individual classes, both models were able to predict classes **1 and 18 most effectively** (car and van). The models differed in their relative acuracy for other classes -- with Model 1 being most inaccurate at predicting **classes 5 and 19** (freight container and wood pallet), and Model 2 being most inaccurate when it came to **classes 7, 10, and 19** (helmet, person, and wood pallet).

**Model 1:**

Best Object Classes: 1, 18

Worst Object Classes: 5, 19

**Model 2:**

Best Object Classes: 1, 18

Worst Object Classes: 7, 10, 19


### 2. Dataset Sampling Strategy (Dataset Design):

**Objective: Determine a sampling strategy for filtering the TechTrack dataset down to 5000+ images.**

**Criteria:**
  - **Mechanism:** Randomly remove images from the dataset until 5000 images remain.
  - Randomly dropping files should roughly preserve class proportions and scene diversity. If significant differences become apparent, re-randomize until differences are within acceptable bounds.

**Justification:**

The charts linked below describe the class diversity present in the dataset pre and post-filtering. Between both datasets, the underlying distribution among class representation remaing roughly the same...

[Dataset Filtering Charts](techtrack/analysis/filtering_charts)


### 3. Threshold Design (Parameter Configuration):

**Objective: Test different NMS IoU thresholds to determine the value which grants the highest mAP value for Model 2 (best performing model)**

Varying the Non-Maximum Suppression (NMS) IoU threshold revealed a strong inverse relationship between the threshold value and overall detection performance over this image dataset...

|IoU Threshold   |mAP    |
|----------------|-------|
|0.0             |0.4254 |
|0.2             |0.4947 |
|0.4             |0.4747 |
|0.6             |0.4253 |
|0.8             |0.2172 |

*Table 2: Comparing Mean-Average Precision (mAP) for Model 2, at differing IoU thresholds*

Model 2 (our best performing model) achieved its highest mAP (0.4947) at an IoU threshold of 0.2, indicating that lower overlap suppression preserved the most true positives. As the threshold increased, mAP tended to decline, before sharply falling to 0.2172 at 0.8.

These results suggest that stricter overlap filtering removes too many valid detections, and that a 0.2-0.4 NMS threshold yields the most accurate predictions for YOLO Model 2.


### 4. Augmentation Impact (Robustness Analysis):

**Objective: Investigate the impact of image augmentation on Model 2's prediction performance.**

|Augmentation                        |mAP    |
|------------------------------------|-------|
|None                                |0.4947 |   
|Brightness (alpha=1, beta=25)       |0.4844 |
|Resize (300, 300)                   |0.0462 |
|Gussian Blur (ksize=(5,5), sigma=0) |0.4343 |
|Horizontal Flip                     |0.2783 |

*Table 3: Comparing Mean-Average Precision (mAP) for Model 2 at [] IoU threshold, given particular image augmentions*

Model 2’s performance varied noticeably under certain augmentation techniques. 
  - Without augmentation, it achieved an mAP of 0.4947. 
  - Introducing **brightness** adjustment caused a slight performance drop (0.4844)
  - **Gaussian blur** decreased mAP (0.4343)
  - **Horizontal flipping** reduced mAP significantly (0.2783)
  - **Resizing to 300×300** severely degraded performance (0.0462)

Overall, mild augmentations had minimal effect, but scale-altering augmentations substantially impacted detection quality at an IoU threshold of 0.2.

***NOTE: Only one example of each type of augmentation was used to build this table. Its possible that certain augmentations have a greater effect on mAP than would otherwise be infered from the table above. For example, making the brightness exponentially higher could have even more of an effect than resizing to (300, 300). Testing every possible augmentation is impossible, and the table above serves only to show a baseline effect stemming from each augmentation.***


### 5. HNM Sampling Strategy (Parameter Configuration):

**Objective: Test multiple different lambda values to idenitfy how they affect the sampling of images**

We use the YOLO loss function as the primary metric for sampling hard negative images for this case study, and adjusting the lambda coefficients alters which images are prioritized for sampling.

Each lambda value weights the contribution of a given loss term, guiding the model to focus on different types of prediction errors:
  - **Increasing LAMBDA_COORD** emphasizes localization errors, sampling images where the model struggles to generate accurate bounding boxes.
  - **Increasing LAMBDA_OBJ** emphasizes objectness errors, selecting images where the model fails to correctly identify the presence of objects.
  - **Increasing LAMBDA_NOOBJ** emphasizes false-positive detections, highlighting images where the model incorrectly predicts objects in background regions.
  - **Increasing LAMBDA_CLS** emphasizes classification errors, identifying images where the model misclassifies object categories.

Each lambda value was raised individually relative to the other values, and the average loss metrics **across 5 sampled hard negative images** were included for comparison:

|lambda coord |lambda obj |lambda noobj |lambda cls |AVG Loc Loss |AVG Conf Obj Loss |AVG Conf Noobj Loss |AVG Class Loss |
|-------------|-----------|-------------|-----------|-------------|------------------|--------------------|---------------|
|0.5          |0.5        |0.5          |0.5        |0.081        |14.23             |0.005               |2.99           |
|**100**      |0.5        |0.5          |0.5        |**0.12**     |10.65             |0.0034              |2.99           |
|0.5          |**100**    |0.5          |0.5        |0.080        |**14.23**         |0.0051              |2.99           |
|0.5          |0.5        |**100**      |0.5        |0.077        |13.72             |**0.0149**          |2.99           |
|0.5          |0.5        |0.5          |**100**    |0.065        |9.214             |0.0034              |**3.023**      |

As we would expect, by raising the lambda weigh for a given component, images are sampled which have a significantly higher loss associated with that component.