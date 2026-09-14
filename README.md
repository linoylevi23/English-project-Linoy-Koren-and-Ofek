# 🎙️ English Speech Recognition & Quality Estimator Pipeline

An end-to-end Machine Learning pipeline and Ground-Truth Annotation Web App for transcribing, aligning, and estimating speech recognition quality for English-learning conversations.

---

## 🚀 Quick Setup for Team Members

Follow these 3 simple steps to get the project running on your computer:

### 1. Clone the Repository
```bash
git clone <YOUR-REPO-URL>
cd PROJECT
```

### 2. Set Up Virtual Environment & Dependencies
```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 3. Connect to Shared Google Drive
Make sure you have **Google Drive for Desktop** installed and synced with the shared folder (`English Recognition Project`).

Then simply run:
```bash
./connect_drive.sh
```
*(If auto-detection fails, pass the path directly: `./connect_drive.sh "/path/to/English Recognition Project"`)*

---

## 🎧 Running the Annotation Web App

To launch the standalone Gradio web app for tagging and inspecting synchronized audio segments:
```bash
./run_app.sh
```
Then open your browser at: **`http://127.0.0.1:7860/`**

---

## 🤖 Running & Training the Machine Learning Models

Open `From_the_Data_Engineering_and_Tagging_notebook_-5.ipynb` in VS Code or Jupyter:
1. You can click **Run All** — the web app cell is enclosed in quotation marks so it will not block execution.
2. **Section 7** will automatically load the ground-truth labeled samples and train 5 benchmark algorithms:
   * **Support Vector Machine (SVM)** (Current leader: ~69.3% Accuracy, 74.7% F1)
   * **Logistic Regression** (~68.3% Accuracy, 72.1% F1)
   * **XGBoost**
   * **Random Forest**
   * **Multi-Layer Perceptron (Neural Network)**

### The 9 Multimodal Features Used:
* **Text Alignment:** `Match_Confidence`, `Missing_Words`, `Different_Words`
* **Acoustic Signals:** `Speech_Volume` (RMS), `Noise_Level` (SNR), `Speech_Rate` (words/sec), `Silence_Before_Turn`
* **Disfluencies:** `Hesitations_Count` (fillers: *"um"*, *"uh"*, repetitions, self-repairs), `Has_Overlap`
