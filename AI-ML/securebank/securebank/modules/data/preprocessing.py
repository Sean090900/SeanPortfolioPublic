# Preprocess dataset: 
import pickle
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE

def temporal_partition(processed_data, p_training=0.7, p_validation=0.15, p_testing=0.15):
    """
    """
    # Check validity of inputs
    assert (p_training + p_validation + p_testing) == 1, 'Partition proportions must add up to 1!'

    # Create initial partitions
    length = len(processed_data)
    training = processed_data[:int(length * p_training)]
    validation = processed_data[int(length * 0.7):int(length * (p_training + p_validation))]
    testing = processed_data[int(length * (1-p_testing)):]

    return training, validation, testing


class Preprocessing:
    """
    """

    def __init__(self):
        self.numeric_transformer = None
        self.categorical_transformer = None
        self.preprocessor = None
        self.is_fitted = False

    def fit(self, train_df, target='is_fraud', one_hot_min_frequency=10000):
        # Seperate features and target
        X_train = train_df.drop(target, axis=1)

        # Split features into numeric and categorical
        numeric_features = X_train.select_dtypes(include=['int64', 'float64']).columns.tolist()
        categorical_features = X_train.select_dtypes(include=['object']).columns.tolist()

        # Setup up preprocessing pipeline for numeric data
        self.numeric_transformer = Pipeline(steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ])

        # Setup up preprocessing pipeline for categorical data
        self.categorical_transformer = Pipeline(steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(min_frequency=one_hot_min_frequency, handle_unknown="ignore", sparse_output=False))
        ])

        # Combine numeric and categorical pipelines into 1 ColumnTransformer
        self.preprocessor = ColumnTransformer(
            transformers=[
                ("num", self.numeric_transformer, numeric_features),
                ("cat", self.categorical_transformer, categorical_features),
            ]
        )
        self.preprocessor.fit(X_train)
        self.is_fitted = True
        return self

    def transform(self, df, target='is_fraud', apply_smote=False, smote_sampling=0.2):
        if self.is_fitted:
            # Seperate features and target
            X = df.drop(target, axis=1)
            y = df[target].astype(int)    # Cast as int, not float

            # Preprocess
            data = self.preprocessor.transform(X)

            # Add 'is_fraud' target back to df
            processed_df = pd.DataFrame(data, columns=self.preprocessor.get_feature_names_out())
            processed_df['is_fraud'] = y.reset_index(drop=True)
        
            # Apply SMOTE to account for class imbalances if specified
            if apply_smote:
                smote = SMOTE(random_state=42, sampling_strategy=smote_sampling)
                X_resampled, y_resmapled = smote.fit_resample(processed_df.drop('is_fraud', axis=1), processed_df['is_fraud'])
                X_resampled['is_fraud'] = y_resmapled
                processed_df = X_resampled.copy()

            return processed_df
        else:
            raise Exception('Must fit pipline with training data before transforming!')
        
    def save(self, dir='./'):
        """
        Utility: Function for saving self as pickle file for later use
        """
        file_name = 'preprocessing_model.pkl'
        with open(dir + file_name, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, path):
        """
        Utility: Function for loading a Preprocessing object from pickle format
        """
        with open(path, 'rb') as f:
            df = pickle.load(f)
        return df
    
    
if __name__ == '__main__':

    df = pd.DataFrame()

    training, validation, testing = temporal_partition(df)

    pre = Preprocessing().fit(training)
    pre.save()

    processed_training = pre.transform(training, apply_smote=True)
    processed_validation = pre.transform(validation)
    processed_testing = pre.transform(testing)