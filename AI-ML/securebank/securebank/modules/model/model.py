import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from xgboost import XGBClassifier

class Model():
    """
    """

    def __init__(self, model_type="rf", n_estimators=200):
        self.trained = False
        self.model_type = model_type
        if model_type == 'rf':
            self.model = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
        elif model_type == 'ada':
            self.model = AdaBoostClassifier(n_estimators=n_estimators, random_state=42)
        elif model_type == 'xgb':
            self.model = XGBClassifier()
        else:
            raise ValueError(f'{model_type} must be one of ["rf", "ada", "xgb"].')
    
    def fit(self, X_train, y_train):
        self.model.fit(X_train, y_train)
        self.trained = True
        return self

    def predict(self, X):
        if not self.trained:
            raise Exception('Must train model before predicting!')
        assert type(X) == pd.DataFrame, "'X' must be a pandas DataFrame!"
        return self.model.predict(X)
    
    def save(self, path):
        """
        Utility: Function for saving self as pickle file for later use
        """
        with open(path, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, path):
        """
        Utility: Function for loading a Model object from pickle format
        """
        with open(path, 'rb') as f:
            df = pickle.load(f)
        return df
    

if __name__ == "__main__":
    model = Model(model_type="random")
    print(model.predict())

