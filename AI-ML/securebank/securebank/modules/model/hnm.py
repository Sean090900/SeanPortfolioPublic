import pandas as pd

def build_hnm_dataset(X_train, y_train, hard_negatives, easy_negatives, easy_frac=0.05):
    """
    Builds the new dataset for training:
    - keep 100% of frauds
    - keep 100% of hard negatives
    - keep a small sample of easy negatives
    """
    frauds = X_train[y_train == 1]

    # Random sample of easy negatives
    easy_sample = easy_negatives.sample(frac=easy_frac, random_state=42)

    # Hard limit of 100,000 hard negatives
    if len(hard_negatives) > 10000:
        hard_negatives = hard_negatives[:10000]

    X_new = pd.concat([frauds, hard_negatives, easy_sample])
    
    # Rebuild labels accordingly
    y_new = pd.concat([
        pd.Series(1, index=frauds.index),
        pd.Series(0, index=hard_negatives.index),
        pd.Series(0, index=easy_sample.index)
    ])

    # Shuffle the dataset
    X_new, y_new = X_new.sample(frac=1, random_state=42), y_new.sample(frac=1, random_state=42)

    return X_new, y_new

def split_negatives_by_difficulty(X_train, y_train, probs, hard_threshold=0.05):
    """
    Splits negative samples into hard and easy buckets.
    
    hard_threshold: 
        - negatives with predicted fraud probability > threshold are "hard"
        - you can raise threshold for more precision, lower for more recall
    """
    negatives = X_train[y_train == 0]
    neg_probs = probs[y_train == 0]

    hard_negatives = negatives[neg_probs > hard_threshold]
    easy_negatives = negatives[neg_probs <= hard_threshold]

    return hard_negatives, easy_negatives

def hard_negative_mining(model, X_train, y_train, hard_threshold=0.05, easy_frac=0.05):
    """
    Full Hard Negative Mining (HNM) pipeline.
    Args:
        model            -> trained classifier that supports predict_proba
        X_train, y_train -> original training data
        hard_threshold   -> probability threshold for hard negatives
        easy_frac        -> fraction of easy negatives to keep
    Returns:
        X_hnm, y_hnm     -> new dataset to retrain your model
    """

    # Step 1: model probabilities
    probs = model.model.predict_proba(X_train)[:, 1]

    # Step 2: split into hard and easy negatives
    hard_negatives, easy_negatives = split_negatives_by_difficulty(
        X_train, y_train, probs, hard_threshold
    )

    # Step 3: rebuild the dataset
    X_hnm, y_hnm = build_hnm_dataset(
        X_train, y_train, hard_negatives, easy_negatives, easy_frac
    )

    print(f"Original dataset size: {len(X_train):,}")
    print(f"Fraud count: {sum(y_train==1):,}")
    print(f"Hard negatives kept: {len(hard_negatives):,}")
    print(f"Easy negatives sampled: {int(len(easy_negatives) * easy_frac):,}")
    print(f"New dataset size: {len(X_hnm):,}")

    return X_hnm, y_hnm