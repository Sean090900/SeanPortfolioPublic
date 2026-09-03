import os
import json
from sklearn.metrics import precision_score, accuracy_score, recall_score, f1_score

def calculate_offline_metrics(y_true, y_pred):
    return {
        'prec': precision_score(y_true, y_pred),
        'rec': recall_score(y_true, y_pred),
        'acc': accuracy_score(y_true, y_pred),
        'f1': f1_score(y_true, y_pred),
    }

def calculate_online_metrics(n_logs, logs_path):
    # Gather list of logs and sort them by most recent
    logs = os.listdir(logs_path)
    logs.sort(reverse=True)
    logs[:n_logs] # Take top 'n' logs

    # Gather information on mean time and mean error rate:
    error_sum = 0
    time_sum = 0
    log_count = 0
    for name in logs:
        log_count += 1
        with open(logs_path + name, 'r') as file:
            log = json.load(file)
            if log['response'] == -1:
                error_sum += 1
            elif log['time']:
                time_sum += log['time']

    # Return error_rate, avg_runtime
    return {
        'error_rate': round(error_sum / log_count, 2), 
        'avg_predict_runtime': round(time_sum / log_count, 2),
    }