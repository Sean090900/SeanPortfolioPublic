# System Report | SecureBank Fraud Detection System

**Author: Sean Dickson**

## Table of Contents
- [1. System Description](#1-system-description)
- [2. Data Design](#2-data-design)
- [3. Model Design](#3-model-design)
- [4. Performance Metrics](#4-performance-metrics)
- [5. Deployment Strategy & Monitoring](#5-deployment-strategy--monitoring)

---

## 1. System Description:

**Objectives:**
  - Explain how the system meets the minimum list of requirements.

This system is designed to provide a reliable, transparent, and continuously improving fraud-detection workflow for SecureBank.    Below is how it satisfies each core requirement.

***1. The system should improve from the previous performance of the model.***

The best-performing model in the system **(XGBClassifier + Hard Negative Mining)** is capable of predicting fraudulent transactions with approximately:

  - **Precision: 0.872**
  - **Recall: 0.812**
  - **F1 Score: 0.841**

... when evaluated on local test data. This significantly improves upon earlier baselines (70% precision and 70% recall).

***2. The system should be able to predict if a given transaction is legitimate or fraudulent.***

The live system runs on a Flask server, where users can POST transaction information to the `/predict` endpoint. The system loads the default model, formats incoming data, runs preprocessing, and returns a prediction indicating whether the transaction appears fraudulent.

***3. The system should allow administrators to generate a new dataset for training from the available data sources.***

Administrators can call the `/create_dataset` endpoint to rebuild the system dataset from raw sources located in `data_sources/`. This enables fast regeneration when new data arrives or when the fraud distribution shifts over time.

***4. The system should allow administrators to support monitoring (i.e., logs).***

All system activity is logged. Each prediction (successful or failed) produces a log entry stored in `storage/logs/`. These logs include:

  - Request query
  - Model response (or error message)
  - Timestamp (in name)
  - Response latency

This allows administrators to monitor system health and diagnose issues.

---

## 2. Data Design:

**Objectives:**
  - Justify feature selection, preprocessing techniques, and data partitioning strategies.
  - Explain how dataset quality is ensured.

**Feature Engineering:**
In addition to the features provided in the raw dataset, the system engineers several behavior-based features that make fraud patterns more learnable. These include:

  - Transaction velocity (frequency of recent transactions)
  - Distance between customer location and merchant location
  - Customer-specific temporal patterns (hour, day, month, etc.)
  - Derived age at time of transaction

These added features help the model understand behavioral irregularities rather than relying solely on static attributes.

**Data Partitioning:**

  - The dataset is partitioned into train/validation/test splits.
  - A **70/15/15** split is used (ough rule of thumb for large datasets).
  - **Temporal partitioning** avoids future data leaking into past model training.
  - Importantly, partitioning is performed before preprocessing, ensuring no leakage from fitted transformers (e.g., one-hot encoder) into validation/test sets.

This approach maintains a realistic simulation of how the model will encounter new, unseen transactions.

**Data Preprocessing:**

Key preprocessing steps include:

  - Dropping rows where **'is_fraud'** is NaN (these cannot be supervised).
  - Fitting the preprocessing pipeline only on the training set, then applying the fitted transform to validation and test sets—this ensures no look-ahead leakage.
  - One-hot encoding categorical features only if they appear at least 10,000 times in the training dataset (pre-SMOTE).
    - This reduces dimensionality, speeds training, and avoids creating thousands of sparse, uninformative columns.

All categorical features were lower-cased before encoding to prevent mismatches from capitalization inconsistencies.

**Ensuring Dataset Quality**
Several measures were taken to ensure training data quality:

  - SMOTE applied only to the training set to handle massive class imbalance (fraud cases are extremely rare).
  - Hard Negative Mining adds difficult non-fraud examples to improve recall and reduce overfitting to too-easy negatives.
  - High-cardinality, non-informative fields—such as `first`, `last`, `street`, and other effectively unique identifiers were removed to prevent overfitting.
  - Direct identifiers like `trans_num` and raw `unix_time` were excluded from model training.
  - All text-based categorical values converted to lowercase to eliminate fragmentary category duplication.

Together, these steps ensure that the data flowing into the system is representative, high-quality, and non-leaky.

---

## 3. Model Design:

**Objectives:**
  - Justify model selection, hyperparameter tuning, and evaluation metrics.
  - Discuss trade-offs between different modeling approaches.

**Model Selection:**
The system includes a model catalogue containing:

  - RandomForestClassifier (sklearn)
  - AdaBoostClassifier (sklearn)
  - XGBClassifier (xgboost)

These were selected because tree-based ensemble models are quite good at handling non-linear boundaries, mixed categorical/numerical data, and large datasets, such as we have for this system.

Additionally, a Hard Negative Mining (HNM) module is included to boost recall by exposing the model to difficult negative samples. This heavily improved model robustness and fraud-capture rate.

**Hyperparameter Tuning:**

RandomForestClassifier & AdaBoostClassifier:

  - **n_estimators = 200** used for both.
    - Increasing the number of trees generally improves stability and variance reduction at the cost of longer training time.

XGBClassifier:

  - The base classifier (default hyperparameters) already outperformed the others.
  - No additional tuning was required for the initial system version.

Hard Negative Mining:
  - **easy_frac**: proportion of easy negatives to keep
  - **hard_threshold**: scoring threshold for labeling difficult negatives

After experimentation, the chosen settings produced the best balance between precision and recall.

**Evaluation Metrics:**

The following evaluation metrics were tracked for monitoring this system:

  - Precision: The accuracy of the system's positive (fraud) predictions.
  - Recall: The ability of the system to find all true positive (fraud) cases.
  - Accuracy: The overall correctness
  - F1 Score: The harmonic mean of precision and recall scores (good for unbalanced datasets)

While working through model selection, precision and recall scores were the metrics I most closely monitored. While both are important to maintain at high levels, I tended to favor models which maximized recall score. A high recall score may mean more false positives, but it will also mean more fraud cases caught. In this implementation, I prioritized catching as many fraud cases as possible over the potential customer-experience difficulties associated with high false-positive rate. 

While I tracked both overall accuracy, the F1 score is a more realistic indicator of how the system is doing since the dataset is very unbalanced. So, while both metrics were tracked, a heavier emphasis was placed on raising F1 score over pure accuracy.

**Trade-Offs between Modeling Approaches**

RandomForestClassifier:
  - Training speed was acceptable (~15min)
  - Good precision and recall, but not as good as XGBClassifier

AdaBoostClassifier:
  - Training too slow (~25min)
  - Lowest Precision and Recall scores

XGBClassifier:
  - Fastest training speed by far (~1min)
  - Displayed highest precision, recall, accuracy, and F1-Score
  - **Selected as the system default**

---

## 4. Performance Metrics:

**Objectives:**
  - Justify your offline metrics
    - Provide experimental results demonstrating the model’s offline performance. 
    - Use tables and graphs to present findings and how they influenced your design.
  - Justify your online performance measurement.
    - Provide a detailed description of how your metrics will be calculated
    - Provide your information collection policy would support the determination of your metrics

**Offline Metrics:**

| Model             | Accuracy      | Precision     | Recall        | F1 Score      |
|-------------------|---------------|---------------|---------------|---------------|
| **Random Forest** | 0.998         | 0.756         | 0.778         | 0.767         |
| **XGBoost**       | 0.999         | 0.872         | 0.812         | 0.841         |
| **AdaBoost**      | 0.994         | 0.308         | 0.680         | 0.424         |

*Accuracy was also calculated, but only as a santity check. F1-Score is a better metric for imbalanced datasets.*

AdaBoost was removed from the final system due to poor performance and impractical training time.

**Online Performance:**

The system measures:

  - Latency of the `/predict` endpoint
  - Error rate (number of failed requests)
  - Model drift indicators (via `/get_health`)

These metrics help determine whether the system remains reliable once deployed in a real environment.

---

## 5. Deployment Strategy & Post-Deployment Monitoring:

**Objectives:**
    - Discuss logging, model error handling, and strategies to detect concept drift or system/model degradation.

**Logging:**

Logs are stored in `storage/logs/`. Each entry corresponds to a single query to the system.

Log contents include:

  - Query payload
  - Model output (or error message)
  - Response time
  - Timestamp (in name)

This provides clean, chronological tracing of all activity.

**Error Handling:**

All prediction logic is wrapped in try/except blocks inside app.py. When an error occurs, the system:

  - Returns an informative message to the user
  - Logs the full error to the logs directory

This makes debugging significantly easier and protects end users from system crashes.

**Detecting Drift:**

The `/get_health `endpoint computes:

  - Offline metrics for all stored models in `storage/models/`
  - Online metrics for the **current default model (XGBClassifier)**

If precision, recall, or F1 scores begin to drop, or latency/error rate rises, these signs may indicate concept drift or system degradation. When drift is detected:

  - A new dataset can be generated via `/create_dataset`
  - A fresh model can be trained via `/train_model`

This ensures long-term adaptability of the fraud detection system.

