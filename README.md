# 🎾 AI-Powered Tennis Video Analysis System

An AI-powered tennis video analysis system that combines Computer Vision, Deep Learning, Object Tracking, and Spatial Analytics to automatically analyze professional tennis matches.

The system detects players and tennis balls, tracks their movement across video frames, generates heatmaps and trajectories, and produces annotated output videos for performance analysis and tactical insights.

---

##  Features

-  Tennis Player Detection
-  Tennis Ball Detection
-  YOLOv8-based Object Detection
-  Court Detection and Spatial Mapping
-  CNN-based Keypoint Extraction
-  Player and Ball Tracking
-  Movement Analysis
-  Heatmap Generation
-  Trajectory Visualization
-  Annotated Video Output
-  Standalone Executable Deployment

---

##  System Pipeline

```text
Input Video
     │
     ▼
YOLOv8 Object Detection
     │
     ▼
Object Tracking
     │
     ▼
CNN Keypoint Detection
     │
     ▼
Video Processing
     │
     ▼
Spatial Analytics
     │
     ▼
Heatmap & Trajectory Generation
     │
     ▼
Output Video
```

---

##  Technologies Used

- Python
- YOLOv8 (Ultralytics)
- PyTorch
- OpenCV
- NumPy
- Pandas
- Matplotlib
- PyInstaller

---

##  Project Structure

```text
Tennis-AI-Analysis/
│
├── input_video/
├── models/
├── trackers/
├── analysis/
├── court_detection/
├── utils/
├── output_videos/
├── heatmaps/
├── trajectories/
├── main.py
├── requirements.txt
└── README.md
```

---

##  Objectives

The system aims to:

- Detect tennis players and balls in match videos.
- Track objects consistently across frames.
- Analyze player movement patterns.
- Generate heatmaps for court coverage.
- Visualize movement trajectories.
- Provide automated sports analytics.
- Deploy as a user-friendly application.

---

##  Generated Outputs

The system automatically generates:

### Player & Ball Detection
- Bounding Boxes
- Confidence Scores

### Tracking Results
- Unique Object IDs
- Continuous Object Tracking

### Analytics
- Player Movement Analysis
- Distance Estimation
- Motion Insights

### Visualizations
- Heatmaps
- Trajectory Maps
- Annotated Match Videos

---

##  Challenges Addressed

This project tackles several challenges in tennis video analysis:

- Small tennis ball detection
- Motion blur
- Fast object movement
- Occlusion handling
- Multi-model integration
- Real-time processing constraints

---

##  Applications

- Tennis Coaching
- Match Analysis
- Player Performance Evaluation
- Sports Research
- Tactical Decision Support

---

##  Future Improvements

- Real-Time Processing Optimization
- Advanced Player Statistics
- Pose Estimation
- Action Recognition
- Event Detection
- Multi-Camera Analysis
- Cloud Deployment
- Mobile Application Support
- AI-Based Tactical Recommendations

---

## 📸 Sample Results

### Detection Output
<img width="1723" height="874" alt="image" src="https://github.com/user-attachments/assets/25a3abaf-467b-49f8-8204-f3ae64e55d10" />

### Heatmap
<img width="1000" height="2000" alt="heatmap" src="https://github.com/user-attachments/assets/206969b7-4c1e-4d03-a667-7302ca1a9996" />


---

##  Research Background

This project was developed as a research-based AI system integrating:

- Deep Learning
- Computer Vision
- Object Tracking
- Spatial Analytics

to automate tennis match analysis and generate meaningful insights from video data.

---

##  Author

**Maryam Emad**

Teaching Assistant & Master's Student in Artificial Intelligence Engineering

Interested in:
- Computer Vision
- Deep Learning
- Sports Analytics
- Machine Learning Applications
