# Intrusion-Detection-System
Overview
This project develops an IoT Intrusion Detection System (IDS) using machine learning techniques to detect network attacks. The system uses the RT-IOT2022 dataset to train and evaluate different algorithms for detecting malicious IoT traffic.
To improve performance, Chi-Squared feature selection is applied to remove irrelevant features, and a hybrid ensemble model combining AdaBoost and Extremely Randomized Trees (ERT) is used for accurate attack detection. The model is deployed using a Flask web application for real-time prediction.
Algorithms Used
KNN (K-Nearest Neighbors)
SVM (Support Vector Machine)
Decision Tree
Gradient Boosting
XGBoost
Random Forest
ERT (Extremely Randomized Trees)
Hybrid Model (AdaBoost + ERT)
Technologies
Python
Scikit-learn
NumPy
Pandas
Matplotlib
Flask
Features
IoT attack detection using machine learning
Feature selection using Chi-Squared method
Hybrid ensemble model for improved accuracy
Real-time attack prediction using Flask web application
Dataset
RT-IOT2022 Dataset
