from flask import Flask, request, jsonify
import os
import json
import time
import pandas as pd
from datetime import datetime
from modules.data.raw_data_handler import RawDataHandler
from modules.data.feature_engineering import (
    calc_dist_between_merch_and_customer,
    calc_age_at_time_of_transaction,
    calc_customer_specific_transaction_trends,
    calc_transaction_velocity
)
from modules.data.preprocessing import Preprocessing, temporal_partition
from modules.model.model import Model
from modules.model.hnm import hard_negative_mining
from modules.model.evaluation import calculate_offline_metrics, calculate_online_metrics

# Config
STORAGE_PATH = 'storage/'
LOGS_PATH = 'storage/logs/'
DATASETS_PATH = 'storage/datasets/'
MODELS_PATH = 'storage/models/'

# Create storage/ directory if not already present
if not os.path.exists(STORAGE_PATH):
    os.mkdir('storage/')

app = Flask(__name__)

# Helper functions
def log_request(query, response, time):
    """
    """
    # Create storage/logs directory if not already present
    if not os.path.exists(LOGS_PATH):
        os.mkdir('storage/logs/')

    # Save query-response combo as json object on storage/logs
        # f"securebank/logs/log_{timestamp}.json"
    log = json.dumps({
        'query': query,
        'response': response,
        'time': time,
    })
    
    # Save log
    timestamp = round(datetime.now().timestamp())
    with open(f'storage/logs/log_{timestamp}.json', 'w') as f:
        f.write(log)

def save_dataset(training, validation, testing):
    """
    """
    # Empty old dataset from storage/datasets
    sets = os.listdir(DATASETS_PATH)
    for set in sets:
        os.remove(f'{DATASETS_PATH}{set}')

    # Save dataset partitions
    timestamp = round(datetime.now().timestamp())
    training.to_csv(DATASETS_PATH + f'dataset_training_{timestamp}.csv', index=False)
    validation.to_csv(DATASETS_PATH + f'dataset_validation_{timestamp}.csv', index=False)
    testing.to_csv(DATASETS_PATH + f'dataset_testing_{timestamp}.csv', index=False)

def load_dataset():
    """
    """
    # Check that dataset exists
    if not os.listdir(DATASETS_PATH):
        raise Exception('Must create dataset first!')
    
    # Load dataset paritions
    training, validation, testing = None, None, None
    for set in os.listdir(DATASETS_PATH):
        set_path = f'{DATASETS_PATH}{set}'
        if 'training' in set_path:
            training = pd.read_csv(set_path)
        elif 'validation' in set_path:
            validation = pd.read_csv(set_path)
        elif 'testing' in set_path:
            testing = pd.read_csv(set_path)
        else:
            raise Exception(f'Dataset: {set_path} is invalid!')
        
    # Check if all three paritions were found
    if any(obj is None for obj in [training, validation, testing]):
        raise Exception('Dataset paritions corrupted! Please re-create your datasets.')
        
    return training, validation, testing


# App routes
@app.route('/')
def info():
    """
    Index route that returns a welcome message.
    Returns: Response with a welcome message.
    """
    return "Welcome to SecureBank Fraud Detection System."

@app.route('/create_dataset', methods=['GET', 'POST'])
def create_dataset():
    start_time = time.time()

    # Initialize handler
    print('Initializing raw data handler...')
    handler = RawDataHandler(storage_path="data_sources", save_path="../../storage/datasets") # DONT NEED SAVE PATH?

    # Extract raw data
    print('Extracting raw data...')
    customer_info, transaction_info, fraud_info = handler.extract(
        "customer_release.csv", "transactions_release.parquet", "fraud_release.json"
    )

    # Transform the data
    print('Transforming data...')
    cleaned_data = handler.transform(customer_info, transaction_info, fraud_info)
    cleaned_data = handler.convert_dates(cleaned_data)

    ### FOR TESTING ###
    # --------------- #
    # cleaned_data = pd.read_csv('../cleaned_data.csv', index_col='Unnamed: 0')
    # --------------- #

    # Save cleaned_data features as csv (this will be necessary during predictions)
    cleaned_data.to_csv(f'{STORAGE_PATH}cleaned_data.csv')

    # Feature Engineering
    print('Feature engineering...')
    cleaned_data = calc_dist_between_merch_and_customer(cleaned_data)
    cleaned_data = calc_age_at_time_of_transaction(cleaned_data)
    cleaned_data = calc_customer_specific_transaction_trends(cleaned_data)
    cleaned_data = calc_transaction_velocity(cleaned_data)

    # Order cleaned_data by unix_time
    print('Preprocessing the data...')
    cleaned_data = cleaned_data.sort_values('unix_time')

    # Drop rows where is_fraud is nan
    cleaned_data = cleaned_data[~cleaned_data['is_fraud'].isna()]

    # Drop unnecesseary ID/Personal columns
    cleaned_data = cleaned_data.drop(['cc_num', 'unix_time', 'first', 'last', 'street', 'trans_num', 'dob', 'zip', 'city', 'minute', 'seconds', 'lat', 'long'], axis=1)

    # Apply lower case to all categorical columns
    cleaned_data = cleaned_data.applymap(lambda x: x.lower() if isinstance(x, str) else x)

    # Split dataset into partitions
    training, validation, testing = temporal_partition(cleaned_data)

    # Fit preprocessing object, save
    pre = Preprocessing().fit(training, one_hot_min_frequency=10000)
    pre.save(STORAGE_PATH)

    # Preprocess partitions
    processed_training = pre.transform(training, apply_smote=True)  # Apply SMOTE for training set only
    processed_validation = pre.transform(validation)
    processed_testing = pre.transform(testing)

    # Save dataset in storage/datasets
    print('Saving dataset partitions...')
    save_dataset(processed_training, processed_validation, processed_testing)

    # Get runtime
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Repsond with JSON body
    print(f'Data Successfully saved to: {DATASETS_PATH}!')
    return jsonify({
        'response': f'Data Successfully saved to: {DATASETS_PATH}!',
        'time': f'{elapsed_time} seconds',
    }), 200

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    start_time = time.time()

    try:
        # Get JSON data from the request
        input_data = request.get_json()

        # Ensure storage/models is not empty and has default model specified!
        if not os.listdir(MODELS_PATH):
            raise Exception('ERROR: Must create at least one model before predicting!')

        # Load model
        print('Loading model...')
        model = Model().load(f'{MODELS_PATH}xgb-hnm.pkl')

        # Convert input_data into single-row df
        print('Formatting input data...')
        info = RawDataHandler(storage_path='', save_path='').convert_dates(pd.Series(input_data).to_frame().T)

        # Get example customer row from training data
        print('Loading template from existing customer data...')
        cleaned_data = pd.read_csv(f'{STORAGE_PATH}cleaned_data.csv', index_col='Unnamed: 0').sort_values('unix_time', ascending=False)
        c_df = cleaned_data[cleaned_data['cc_num'] == input_data['cc_num']]
        c_df = c_df[~c_df['is_fraud'].isna()].reset_index(drop=True)

        if len(c_df) != 0:
            # Build from existing customer rows
            print('Build new data from existing customer...')
            template = c_df[:1].copy()
            for col in template.columns:
                if col in info.columns:
                    template.at[0, col] = info.loc[0, col]
            input = template.copy()

            # Feature Engineering to match training set
            print('Feature engineering...')
            input = calc_dist_between_merch_and_customer(input)
            input = calc_age_at_time_of_transaction(input)
            input = calc_customer_specific_transaction_trends(input)
            input = calc_transaction_velocity(input)

            # Preprocessing to match training set
            print('Preprocessing to match training data...')
            # Order cleaned_data by unix_time
            input = input.sort_values('unix_time')
            # Drop unnecesseary ID/Personal columns
            input = input.drop(['cc_num', 'unix_time', 'first', 'last', 'street', 'trans_num', 'dob', 'zip', 'city', 'minute', 'seconds', 'lat', 'long'], axis=1)
            # Apply lower case to all categorical columns
            input = input.applymap(lambda x: x.lower() if isinstance(x, str) else x)
            # Load preprocessor and process input
            pre = Preprocessing().load(f'{STORAGE_PATH}preprocessing_model.pkl')
            processed_input = pre.transform(input)

            # Model prediction
            print('Making prediction...')
            pred_value = int(model.predict(processed_input.drop('is_fraud', axis=1))[0])

            # Get runtime
            end_time = time.time()
            elapsed_time = end_time - start_time

            log_request(input_data, pred_value, elapsed_time)
            if pred_value == 0:
                return jsonify({
                    'predict': 'legitimate',
                    'time': f'{elapsed_time} seconds',
                }), 200
            elif pred_value == 1:
                return jsonify({
                    'predict': 'fraudulent',
                    'time': f'{elapsed_time} seconds',
                }), 200
            else:
                raise Exception(f'Something went wrong... {pred_value} is unacceptable outcome...')
            
        else:
            raise Exception('Customer not found!')  # Eventually, this should be implemented!
    
    except Exception as e:
        log_request(input_data, -1, None)   # -1 means error!
        return jsonify({
            'predict': None,
            'time': None,
            'error': f'An error accured: {e}'
        }), 400

        
@app.route('/train_model', methods=['GET', 'POST'])
def train_model():
    start_time = time.time()

    # Get JSON data from the request
    input_data = request.get_json()
    model_type = input_data['model_type']

    # Load datasets
    print('Loading/splitting dataset...')
    training, _, _ = load_dataset()

    # Split dataset
    X_train = training.drop('is_fraud', axis=1)
    y_train = training["is_fraud"]

    # Train base model
    print('Training base model...')
    try:
        model = Model(model_type=model_type).fit(X_train, y_train)
    except Exception as e:
        return jsonify({'error': f'Could not generate base model of type: {model_type}'}), 400

    # Apply Hard Negative Mining
    print('Applying hard negative mining...')
    X_hnm, y_hnm = hard_negative_mining(model, X_train, y_train,
        hard_threshold=0.07,   # 0.07 found to be optimal through hyperparameter tuning
        easy_frac=0.07         # 0.07 found to be optimal through hyperparameter tuning
    )

    # Retrain a new model on the HNM dataset
    if model_type == 'rf' or model_type == 'ada':
        hnm_model = Model(model_type=model_type, n_estimators=300)    # Raise estimators since dealing with smaller dataset now
    else:
        hnm_model = Model(model_type=model_type)                      # No n_estimators param for XGBoostClassifier
    hnm_model.fit(X_hnm, y_hnm)

    # Save model to storage/models
    print('Saving model...')
    hnm_model.save(MODELS_PATH + f'{model_type}-hnm.pkl')

    # Get runtime
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Return json response
    return jsonify({
        'response': "Model trained successfully!",
        'time': f'{elapsed_time} seconds',
    }), 200

@app.route('/get_health', methods=['GET', 'POST'])
def get_health():
    # Create health info response body
    info = {}

    # Load testing dataset
    print('Loading test set...')
    _, _, testing = load_dataset()

    # Split dataset
    X_test = testing.drop('is_fraud', axis=1)
    y_test = testing['is_fraud']

    # Get offline metrics for all models
    print('Gathering offline metrics for each model...')
    for file_name in os.listdir(MODELS_PATH):
        model = Model().load(MODELS_PATH + file_name)
        y_pred = model.predict(X_test)
        info[file_name] = calculate_offline_metrics(y_test, y_pred)

    # Get online metrics for default model
    print('Gathering online metrics for defaul system model...')
    info['online_metrics_xgb_default'] = calculate_online_metrics(10, LOGS_PATH)

    # Return metrics
    return jsonify(info)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)