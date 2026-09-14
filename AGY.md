# Antigravity Workspace Guide: English Speech Recognition Project

## Overview
This repository contains an end-to-end data engineering, speech transcription, manual annotation, and quality estimation machine learning pipeline.

## Architecture & Layout
- `From_the_Data_Engineering_and_Tagging_notebook_-5.ipynb`: The main end-to-end Jupyter Notebook covering ingestion, Whisper acoustic transcription, ChatGPT alignment, acoustic feature extraction, and ML model training.
- `app.py`: Standalone Gradio tagging application for ground-truth data annotation.
- `run_app.sh`: Bash runner for the web app with virtualenv auto-activation.
- `connect_drive.sh`: Links local Google Drive cloud folder to `Audio/` and `Transcripts/`.
- `requirements.txt`: Python package specifications.

## Key Data Sources (Google Drive Synced)
- `Audio/`: Raw student audio recordings (`.m4a` files formatted as `{Condition}_{StudentID}_{SessionNum}_audio.m4a`).
- `Transcripts/Final_Master_Database.xlsx`: Master unified database with extracted acoustic/linguistic features and `Human_Label` ground-truth annotations.

## Machine Learning Details
- Target variable: `Human_Label`
  - Task A (Binary): `0` = Valid (`תקין`), `1` = Needs Correction (`נדרש תיקון`)
  - Task B (3-Class): `0` = Valid, `1` = Minor Correction, `2` = Major Correction
- Features (9 Multimodal):
  - `Match_Confidence`, `Speech_Volume`, `Noise_Level`, `Speech_Rate`, `Silence_Before_Turn`, `Hesitations_Count`, `Missing_Words`, `Different_Words`, `Has_Overlap`.
- Benchmark models evaluated via 5-Fold Stratified Cross-Validation: Logistic Regression, Random Forest, XGBoost, SVM (RBF), MLP.
