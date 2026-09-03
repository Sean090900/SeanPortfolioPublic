# Make the POST request
curl -X POST http://127.0.0.1:5000/train_model \
     -H "Content-Type: application/json" \
     -d '{"model_type": "xgb"}'
