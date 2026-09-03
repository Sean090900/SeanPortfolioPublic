### Techtrack | Computer Vision App

#### Overview

This project implements a modular object detection pipeline designed to evaluate and improve YOLO-based models through systematic inference, hard negative mining, and mAP evaluation. The goal is to deploy a fully functional Inference Service and Rectification Service that can process live video streams, refine model accuracy, and provide interpretable performance metrics — all within a Dockerized container for reproducible deployment.

#### Objectives / Goals

By the end of this project, the system will be able to:
  - Implement and extend the Inference Service for object detection.
  - Implement the Rectification Service for hard negative mining.
  - Evaluate model performance using Mean Average Precision (mAP).
  - Deploy the entire pipeline as a Dockerized Inference Service.

#### Project Structure

techtrack/

│

├── modules/              # Python modules 

├── storage/              # Dataset/YOLO Model files

├── analysis/             # Analysis notebooks/charts

├── app.py                # Execution script for video capture

├── Dockerfile            # Docker Image file

└── README.md             # This file

#### Usage

Build the Docker Image:
```bash
docker build -t techtrack-image .
```

Run Docker Container:
```bash
docker run -it -p 23000:23000/udp techtrack-image
```

Stream Video using FFmpeg:
```bash
ffmpeg -re -i ./test_videos/worker-zone-detection.mp4 -r 30 -vcodec mpeg4 -f mpegts udp://127.0.0.1:23000
```

Test API Endpoints:
```bash
curl http://localhost:5000/predict -X POST -F "file=@frame.jpg"
```