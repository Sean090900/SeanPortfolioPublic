**Quick start instructions** for starting the server with Docker  

The **curl command** you used to test predictions  
`curl -X POST -H "Content-Type: application/json"`
`docker build -t`
`docker run -p 5000:5000`



The most interesting technical personal project I’ve completed was another school project called SecureBank: a full fraud-detection pipeline I built end-to-end using real-world-style financial transaction data. Instead of treating it as a basic classification exercise, I built it like a production-ready ML system.

I began by engineering features for a transactional dataset with temporal structure, merchant embeddings, behavioral information, and simulated fraud patterns that evolved over time. Then I implemented a multi-model training stack (Random Forest, XGBoost, and a custom PyTorch MLP) evaluated with cross-validation and drift analysis. To make the system more realistic, I engineered sequential features like rolling averages, days-since-last-transaction, and category-level spending vectors.

What I found most interesting was building the feature orchestration layer: an ingest → transform → encode pipeline that handled categorical hashing, anomaly-score injection, and class-imbalance correction without leaking future information. I also built a small API that accepted transaction events and returned real-time fraud predictions.

This project blended ML modeling, data engineering, real-time inference, and system design—and felt very close to the kind of applied ML infrastructure companies use in production.