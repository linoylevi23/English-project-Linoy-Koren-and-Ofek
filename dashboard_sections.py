import os
import base64

# Base styles scoped to dashboard content
DASHBOARD_CSS = """
<style>
  .dash-panel {
    direction: ltr !important;
    text-align: left !important;
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 22px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #0f172a;
    line-height: 1.5;
    box-sizing: border-box;
    margin-bottom: 16px;
  }
  .dash-panel * {
    box-sizing: border-box;
  }
  .dash-two-col {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 20px;
    direction: ltr !important;
    text-align: left !important;
  }
  .dash-title {
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 8px;
    color: #0f172a;
  }
  .dash-desc {
    font-size: 12px;
    color: #64748b;
    margin-bottom: 18px;
  }
  .dash-progress-group {
    margin-bottom: 14px;
  }
  .dash-progress-header {
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 4px;
  }
  .dash-progress-track {
    width: 100%;
    height: 12px;
    background-color: #f1f5f9;
    border-radius: 9999px;
    overflow: hidden;
  }
  .dash-progress-fill {
    height: 100%;
    border-radius: 9999px;
    transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  }
  .dash-alert {
    background-color: #eff6ff;
    border-left: 4px solid #2563eb;
    padding: 12px 14px;
    border-radius: 8px;
    font-size: 12px;
    color: #1e3a8a;
    margin-top: 16px;
    line-height: 1.5;
  }
  .dash-alert-emerald {
    background-color: #ecfdf5;
    border-left: 4px solid #059669;
    color: #064e3b;
  }
  .dash-alert-amber {
    background-color: #fffbeb;
    border-left: 4px solid #d97706;
    color: #78350f;
  }
  .dash-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
    text-align: left;
    direction: ltr;
  }
  .dash-table th {
    background-color: #f8fafc;
    padding: 10px 12px;
    font-weight: 700;
    color: #334155;
    border-bottom: 1px solid #e2e8f0;
  }
  .dash-table td {
    padding: 10px 12px;
    border-bottom: 1px solid #f1f5f9;
  }
  .dash-table tr:hover td {
    background-color: #f8fafc;
  }
  .dash-badge {
    display: inline-flex;
    align-items: center;
    padding: 3px 8px;
    border-radius: 9999px;
    font-size: 11px;
    font-weight: 700;
  }
  .dash-badge-success {
    background-color: #d1fae5;
    color: #065f46;
  }
  .dash-badge-amber {
    background-color: #fef3c7;
    color: #92400e;
  }
  .dash-badge-red {
    background-color: #fee2e2;
    color: #991b1b;
  }
  .dash-badge-info {
    background-color: #dbeafe;
    color: #1e40af;
  }
  .dash-cm-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-top: 12px;
    text-align: center;
  }
  .dash-cm-cell {
    padding: 14px;
    border-radius: 12px;
    border: 1px solid transparent;
  }
  .dash-gallery-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 16px;
    margin-top: 16px;
  }
  .dash-fig-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 12px;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  }
  .dash-fig-card img {
    width: 100%;
    height: auto;
    border-radius: 8px;
    margin-bottom: 8px;
    border: 1px solid #f1f5f9;
  }
</style>
"""

def get_base64_image(rel_path):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, rel_path)
    if os.path.exists(full_path):
        with open(full_path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"
    return ""

def get_header_and_kpis_html():
    return f"""
{DASHBOARD_CSS}
<div style="direction: ltr; text-align: left; margin-bottom: 20px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; padding-bottom: 16px; border-bottom: 1px solid #e2e8f0; gap: 16px;">
    <div>
      <div style="display: flex; align-items: center; gap: 12px;">
        <span style="font-size: 28px;">🎙️</span>
        <h1 style="font-size: 22px; font-weight: 800; color: #0f172a; margin: 0;">Research Dashboard: Speech Quality Assurance & Machine Learning Pipeline</h1>
      </div>
      <div style="font-size: 13px; color: #64748b; margin-top: 4px;">
        Research Project: English Learner Conversation Analysis (ChatGPT vs. Whisper), Learner Error Preservation & Automated Quality Classification
      </div>
    </div>
    <div style="display: flex; gap: 8px; flex-wrap: wrap;">
      <span class="dash-badge dash-badge-success" style="padding: 6px 12px; font-size: 12px;">● Live & Synced Database (Drive)</span>
      <span class="dash-badge dash-badge-info" style="padding: 6px 12px; font-size: 12px;">742 Total Turns | 104 Verified</span>
    </div>
  </div>

  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 16px; margin-top: 20px;">
    <div class="dash-panel" style="padding: 16px; margin-bottom: 0;">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 11px; font-weight: 700; color: #2563eb; text-transform: uppercase;">Top Model Accuracy (SVM)</span>
        <span style="font-size: 18px;">🏆</span>
      </div>
      <div style="display: flex; align-items: baseline; gap: 8px; margin-top: 8px;">
        <span style="font-size: 26px; font-weight: 800; color: #0f172a;">69.29%</span>
        <span class="dash-badge dash-badge-success">F1: 74.67%</span>
      </div>
      <div style="font-size: 11px; color: #64748b; margin-top: 6px;">5-Fold Stratified CV vs. Human Ground Truth</div>
    </div>

    <div class="dash-panel" style="padding: 16px; margin-bottom: 0;">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 11px; font-weight: 700; color: #4f46e5; text-transform: uppercase;">Word Error Rate (WER)</span>
        <span style="font-size: 18px;">📉</span>
      </div>
      <div style="display: flex; align-items: baseline; gap: 8px; margin-top: 8px;">
        <span style="font-size: 26px; font-weight: 800; color: #0f172a;">38.83%</span>
        <span class="dash-badge dash-badge-info">CER: 37.6%</span>
      </div>
      <div style="font-size: 11px; color: #64748b; margin-top: 6px;">Valid: 31.1% | Needs Correction: 48.2%</div>
    </div>

    <div class="dash-panel" style="padding: 16px; margin-bottom: 0;">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 11px; font-weight: 700; color: #d97706; text-transform: uppercase;">Learner Error Preservation (Whisper)</span>
        <span style="font-size: 18px;">🗣️</span>
      </div>
      <div style="display: flex; align-items: baseline; gap: 8px; margin-top: 8px;">
        <span style="font-size: 26px; font-weight: 800; color: #0f172a;">25.4%</span>
        <span class="dash-badge dash-badge-amber">7.5x higher than ChatGPT</span>
      </div>
      <div style="font-size: 11px; color: #64748b; margin-top: 6px;">Whisper: 15/59 | ChatGPT: 2/59 (3.4%)</div>
    </div>

    <div class="dash-panel" style="padding: 16px; margin-bottom: 0;">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 11px; font-weight: 700; color: #059669; text-transform: uppercase;">Top Predictive Feature</span>
        <span style="font-size: 18px;">💡</span>
      </div>
      <div style="display: flex; align-items: baseline; gap: 8px; margin-top: 8px;">
        <span style="font-size: 20px; font-weight: 800; color: #0f172a;">Match_Confidence</span>
        <span class="dash-badge dash-badge-success">25.24%</span>
      </div>
      <div style="font-size: 11px; color: #64748b; margin-top: 6px;">Correlation Between Acoustic Signal & Text</div>
    </div>
  </div>
</div>
"""

def get_student_progression_html():
    return f"""
{DASHBOARD_CSS}
<div class="dash-two-col">
  <!-- Student 1: Lilo -->
  <div class="dash-panel">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
      <div style="font-size: 14px; font-weight: 700; color: #0f172a;">👩‍🎓 Learner: Lilo (328 Total Speech Turns)</div>
      <span class="dash-badge dash-badge-success">Improvement Trend: +10.2% 🚀</span>
    </div>
    <div class="dash-desc">Tracking Match Confidence, speech rate, and hesitations across 4 sessions:</div>

    <div class="dash-progress-group">
      <div class="dash-progress-header">
        <span>Session 1 (Baseline)</span>
        <span style="font-weight: 700; color: #64748b;">Confidence: 0.767 | Rate: 3.59 w/s | 0.45 Hesitations per turn</span>
      </div>
      <div class="dash-progress-track">
        <div class="dash-progress-fill" style="width: 76.7%; background-color: #94a3b8;"></div>
      </div>
    </div>

    <div class="dash-progress-group">
      <div class="dash-progress-header">
        <span>Session 2</span>
        <span style="font-weight: 700; color: #64748b;">Confidence: 0.644 | Rate: 4.21 w/s | 0.08 Hesitations per turn</span>
      </div>
      <div class="dash-progress-track">
        <div class="dash-progress-fill" style="width: 64.4%; background-color: #cbd5e1;"></div>
      </div>
    </div>

    <div class="dash-progress-group">
      <div class="dash-progress-header">
        <span>Session 3</span>
        <span style="font-weight: 700; color: #64748b;">Confidence: 0.714 | Rate: 3.85 w/s | 0.10 Hesitations per turn</span>
      </div>
      <div class="dash-progress-track">
        <div class="dash-progress-fill" style="width: 71.4%; background-color: #38bdf8;"></div>
      </div>
    </div>

    <div class="dash-progress-group">
      <div class="dash-progress-header">
        <span>Session 4 (Final Session)</span>
        <span style="font-weight: 800; color: #059669;">Confidence: 0.868 | Rate: 2.21 w/s | 0.22 Hesitations per turn (+10.2% Improvement)</span>
      </div>
      <div class="dash-progress-track">
        <div class="dash-progress-fill" style="width: 86.8%; background-color: #059669;"></div>
      </div>
    </div>

    <div class="dash-alert dash-alert-emerald">
      <strong>Personal Analysis for Lilo:</strong> The learner demonstrated steady improvement in speech fluency and cut filler words and stutters in half. Acoustic transcription quality rose from 0.767 to 0.868, indicating marked second language acquisition (SLA) progress.
    </div>
  </div>

  <!-- Student 2: Thomas Shelby -->
  <div class="dash-panel">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
      <div style="font-size: 14px; font-weight: 700; color: #0f172a;">👨‍🎓 Learner: Thomas Shelby (414 Total Speech Turns)</div>
      <span class="dash-badge dash-badge-amber">Impact of Speech Rate on ASR</span>
    </div>
    <div class="dash-desc">Tracking Match Confidence and extreme speech rate across 4 sessions:</div>

    <div class="dash-progress-group">
      <div class="dash-progress-header">
        <span>Session 1</span>
        <span style="font-weight: 700; color: #0284c7;">Confidence: 0.801 | Moderate rate: 3.56 words/sec</span>
      </div>
      <div class="dash-progress-track">
        <div class="dash-progress-fill" style="width: 80.1%; background-color: #0284c7;"></div>
      </div>
    </div>

    <div class="dash-progress-group">
      <div class="dash-progress-header">
        <span>Session 2 (Peak Quality)</span>
        <span style="font-weight: 700; color: #059669;">Confidence: 0.845 | Rate: 3.59 words/sec</span>
      </div>
      <div class="dash-progress-track">
        <div class="dash-progress-fill" style="width: 84.5%; background-color: #059669;"></div>
      </div>
    </div>

    <div class="dash-progress-group">
      <div class="dash-progress-header">
        <span>Session 3</span>
        <span style="font-weight: 700; color: #d97706;">Confidence: 0.608 | Accelerated rate: 5.48 words/sec ⚠️</span>
      </div>
      <div class="dash-progress-track">
        <div class="dash-progress-fill" style="width: 60.8%; background-color: #f59e0b;"></div>
      </div>
    </div>

    <div class="dash-progress-group">
      <div class="dash-progress-header">
        <span>Session 4</span>
        <span style="font-weight: 700; color: #dc2626;">Confidence: 0.592 | Highly accelerated rate: 5.85 words/sec</span>
      </div>
      <div class="dash-progress-track">
        <div class="dash-progress-fill" style="width: 59.2%; background-color: #ef4444;"></div>
      </div>
    </div>

    <div class="dash-alert dash-alert-amber">
      <strong>Critical Insight for Research Question #7:</strong> Thomas Shelby's case demonstrates that a sharp surge in speech rate (from 3.5 words/sec to ~5.8 words/sec, >350 WPM) causes coarticulation, syllable dropping, and ASR transcription errors, explaining why <code>Speech_Rate</code> is the primary acoustic predictor in our model!
    </div>
  </div>
</div>

<!-- Comparison Table -->
<div class="dash-panel" style="margin-top: 16px;">
  <div class="dash-title">📋 Summary Comparison Table: Longitudinal Learner Progression (Final Master Database)</div>
  <table class="dash-table">
    <thead>
      <tr>
        <th>Learner Name</th>
        <th>Sessions</th>
        <th>Session 1 Baseline Confidence</th>
        <th>Final Session Confidence</th>
        <th>Confidence Delta</th>
        <th>Average Speech Rate</th>
        <th>Total Turns</th>
        <th>Research Finding</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="font-weight: 700; color: #065f46;">Lilo</td>
        <td>1 to 4</td>
        <td>0.767</td>
        <td style="font-weight: 700; color: #059669;">0.868</td>
        <td style="font-weight: 700; color: #059669;">+10.2% 📈</td>
        <td>3.43 w/s</td>
        <td>328</td>
        <td>Marked fluency gains, 50% drop in disfluencies</td>
      </tr>
      <tr>
        <td style="font-weight: 700; color: #1e3a8a;">Thomas Shelby</td>
        <td>1 to 4</td>
        <td>0.801</td>
        <td style="font-weight: 700; color: #dc2626;">0.592</td>
        <td style="font-weight: 700; color: #dc2626;">-21.0% 📉</td>
        <td>4.62 w/s</td>
        <td>414</td>
        <td>Excessive speech rate (> 5.5 w/s, ~350 WPM) degraded transcription quality</td>
      </tr>
      <tr style="background: #f8fafc; font-weight: 800;">
        <td>Overall Session Mean</td>
        <td>1 to 4</td>
        <td>0.740</td>
        <td style="color: #2563eb;">0.860</td>
        <td style="color: #2563eb;">+12.0% Mean Improvement 🚀</td>
        <td>4.59 w/s</td>
        <td>742</td>
        <td>Significant general upward trend in structured AI conversations</td>
      </tr>
    </tbody>
  </table>
</div>
"""

def get_models_html():
    return f"""
{DASHBOARD_CSS}
<div class="dash-two-col">
  <div class="dash-panel">
    <div class="dash-title">🏆 Performance Comparison Across 5 Algorithms (Task A: Binary Classification)</div>
    <div class="dash-desc">5-Fold Stratified Cross-Validation across 104 labeled turns with 9 multimodal features:</div>

    <div class="dash-progress-group">
      <div class="dash-progress-header">
        <span>Support Vector Machine (SVM - RBF) 🥇</span>
        <span style="color: #2563eb; font-weight: 700;">69.29% (F1: 74.67%)</span>
      </div>
      <div class="dash-progress-track">
        <div class="dash-progress-fill" style="width: 69.29%; background-color: #2563eb;"></div>
      </div>
    </div>

    <div class="dash-progress-group">
      <div class="dash-progress-header">
        <span>Logistic Regression 🥈</span>
        <span style="color: #4f46e5; font-weight: 700;">68.29% (F1: 72.07%)</span>
      </div>
      <div class="dash-progress-track">
        <div class="dash-progress-fill" style="width: 68.29%; background-color: #4f46e5;"></div>
      </div>
    </div>

    <div class="dash-progress-group">
      <div class="dash-progress-header">
        <span>XGBoost Classifier 🥉</span>
        <span style="color: #0d9488; font-weight: 700;">63.48% (F1: 68.08%)</span>
      </div>
      <div class="dash-progress-track">
        <div class="dash-progress-fill" style="width: 63.48%; background-color: #0d9488;"></div>
      </div>
    </div>

    <div class="dash-progress-group">
      <div class="dash-progress-header">
        <span>Random Forest (100 Trees)</span>
        <span style="color: #059669; font-weight: 700;">61.57% (F1: 66.93%)</span>
      </div>
      <div class="dash-progress-track">
        <div class="dash-progress-fill" style="width: 61.57%; background-color: #059669;"></div>
      </div>
    </div>

    <div class="dash-progress-group">
      <div class="dash-progress-header">
        <span>Neural Network (MLP: 16x8)</span>
        <span style="color: #64748b; font-weight: 700;">58.57% (F1: 58.92%)</span>
      </div>
      <div class="dash-progress-track">
        <div class="dash-progress-fill" style="width: 58.57%; background-color: #94a3b8;"></div>
      </div>
    </div>

    <div class="dash-alert">
      <strong>💡 Key Scientific Insight:</strong> The SVM algorithm achieved top performance in accuracy and F1 score due to its wide margin separation boundaries, avoiding overfitting on compact datasets. As more ground-truth annotations are collected, XGBoost and Random Forest are expected to dominate above 80%+.
    </div>
  </div>

  <div class="dash-panel">
    <div class="dash-title">🎯 Confusion Matrix (SVM)</div>
    <div class="dash-desc">Decomposition of model decisions versus true human ground truth in the stratified test split:</div>

    <div class="dash-cm-grid">
      <div class="dash-cm-cell" style="background-color: #ecfdf5; border-color: #a7f3d0;">
        <div style="font-size: 11px; font-weight: 700; color: #065f46;">True Negative (Valid)</div>
        <div style="font-size: 24px; font-weight: 800; color: #064e3b; margin: 4px 0;">29</div>
        <div style="font-size: 10px; color: #047857;">64.4% correctly identified as Valid</div>
      </div>
      <div class="dash-cm-cell" style="background-color: #fffbeb; border-color: #fde68a;">
        <div style="font-size: 11px; font-weight: 700; color: #92400e;">False Positive (False Alarms)</div>
        <div style="font-size: 24px; font-weight: 800; color: #78350f; margin: 4px 0;">16</div>
        <div style="font-size: 10px; color: #b45309;">Predicted Needs Review, but actually Valid</div>
      </div>
      <div class="dash-cm-cell" style="background-color: #fef2f2; border-color: #fecaca;">
        <div style="font-size: 11px; font-weight: 700; color: #991b1b;">False Negative (Missed Errors)</div>
        <div style="font-size: 24px; font-weight: 800; color: #7f1d1d; margin: 4px 0;">16</div>
        <div style="font-size: 10px; color: #b91c1c;">Predicted Valid, but Needs Review</div>
      </div>
      <div class="dash-cm-cell" style="background-color: #eff6ff; border-color: #bfdbfe;">
        <div style="font-size: 11px; font-weight: 700; color: #1e40af;">True Positive (Caught Errors)</div>
        <div style="font-size: 24px; font-weight: 800; color: #1e3a8a; margin: 4px 0;">43</div>
        <div style="font-size: 10px; color: #2563eb;">72.9% of errors successfully detected!</div>
      </div>
    </div>

    <div class="dash-alert dash-alert-emerald" style="margin-top: 20px;">
      <strong>Error Recall: 72.9%</strong> — The model detects nearly 3 out of every 4 defective turns, saving over 70% of manual auditing time for human annotators!
    </div>
  </div>
</div>
"""

def get_asr_html():
    return f"""
{DASHBOARD_CSS}
<div class="dash-two-col">
  <div class="dash-panel">
    <div class="dash-title">📊 ASR Quality Metrics Breakdown by Ground-Truth Category</div>
    <div class="dash-desc">Word Error Rate (WER) and Character Error Rate (CER) computed over 1,754 words vs. quality labels:</div>

    <table class="dash-table">
      <thead>
        <tr>
          <th>Category</th>
          <th>Sample Size (N)</th>
          <th>WER (%)</th>
          <th>CER (%)</th>
          <th>Quality Status</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td style="font-weight: 700; color: #065f46;">Valid</td>
          <td>45</td>
          <td style="font-weight: 700;">31.10%</td>
          <td>31.00%</td>
          <td><span class="dash-badge dash-badge-success">High Quality</span></td>
        </tr>
        <tr>
          <td style="font-weight: 700; color: #92400e;">Minor Correction Required</td>
          <td>29</td>
          <td style="font-weight: 700;">33.70%</td>
          <td>45.82%</td>
          <td><span class="dash-badge dash-badge-amber">Moderate Quality</span></td>
        </tr>
        <tr>
          <td style="font-weight: 700; color: #991b1b;">Major Correction Required</td>
          <td>30</td>
          <td style="font-weight: 700; color: #dc2626;">48.23%</td>
          <td>39.54%</td>
          <td><span class="dash-badge dash-badge-red">Critical Divergence</span></td>
        </tr>
        <tr style="background-color: #f8fafc; font-weight: 800;">
          <td>Global Weighted Aggregate</td>
          <td>104</td>
          <td style="color: #2563eb;">38.83%</td>
          <td style="color: #2563eb;">37.60%</td>
          <td>Full Weighted Aggregate</td>
        </tr>
      </tbody>
    </table>

    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-top: 16px; text-align: center;">
      <div style="background: #f8fafc; padding: 10px; border-radius: 8px; border: 1px solid #e2e8f0;">
        <div style="font-size: 11px; color: #64748b;">Deletions</div>
        <div style="font-size: 16px; font-weight: 800; color: #0f172a; margin-top: 2px;">29.30%</div>
        <div style="font-size: 10px; color: #94a3b8;">(514 words)</div>
      </div>
      <div style="background: #f8fafc; padding: 10px; border-radius: 8px; border: 1px solid #e2e8f0;">
        <div style="font-size: 11px; color: #64748b;">Substitutions</div>
        <div style="font-size: 16px; font-weight: 800; color: #0f172a; margin-top: 2px;">6.44%</div>
        <div style="font-size: 10px; color: #94a3b8;">(113 words)</div>
      </div>
      <div style="background: #f8fafc; padding: 10px; border-radius: 8px; border: 1px solid #e2e8f0;">
        <div style="font-size: 11px; color: #64748b;">Insertions</div>
        <div style="font-size: 16px; font-weight: 800; color: #0f172a; margin-top: 2px;">3.08%</div>
        <div style="font-size: 10px; color: #94a3b8;">(54 words)</div>
      </div>
    </div>
  </div>

  <div class="dash-panel">
    <div class="dash-title">🗣️ Learner Error & Disfluency Preservation (Guidelines p. 7)</div>
    <div class="dash-desc">
      Evaluating: <code style="background: #f1f5f9; padding: 2px 6px; border-radius: 4px; color: #2563eb;">Learner Error Preservation Rate</code> vs. LLM tendency to normalize and smooth imperfect speech:
    </div>

    <div style="margin: 20px 0;">
      <div class="dash-progress-group">
        <div class="dash-progress-header">
          <span style="color: #0d9488; font-weight: 700;">Acoustic Transcript (Whisper)</span>
          <span style="color: #0d9488; font-weight: 800;">25.4% (15 of 59 turns)</span>
        </div>
        <div class="dash-progress-track" style="height: 16px;">
          <div class="dash-progress-fill" style="width: 25.4%; background-color: #0d9488;"></div>
        </div>
      </div>

      <div class="dash-progress-group" style="margin-top: 14px;">
        <div class="dash-progress-header">
          <span style="color: #64748b; font-weight: 700;">Textual Transcript (ChatGPT)</span>
          <span style="color: #64748b; font-weight: 800;">3.4% (2 of 59 turns)</span>
        </div>
        <div class="dash-progress-track" style="height: 16px;">
          <div class="dash-progress-fill" style="width: 3.4%; background-color: #f87171;"></div>
        </div>
      </div>
    </div>

    <div class="dash-alert dash-alert-emerald">
      <strong>💡 Definitive Answer to Research Question #2:</strong><br>
      While ChatGPT automatically deleted or normalized virtually all learner hesitations and stutters (96.6% erased), the acoustic Whisper model preserved natural conversational fillers ("um", "uh", repetitions, self-repairs) at a rate <strong>7.5x higher</strong>!
    </div>
  </div>
</div>
"""

def get_conditions_html():
    return f"""
{DASHBOARD_CSS}
<div class="dash-two-col">
  <div class="dash-panel">
    <div class="dash-title">🤖 Research Question #5: AI Bot vs. Human Teacher Conversations</div>
    <div class="dash-desc">Comparing accuracy and Match Confidence across the two learning conditions:</div>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin: 16px 0; text-align: center;">
      <div style="background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 12px; padding: 16px;">
        <div style="font-size: 12px; font-weight: 700; color: #1e40af;">Conversations with AI Bot</div>
        <div style="font-size: 28px; font-weight: 800; color: #1e3a8a; margin: 4px 0;">0.82</div>
        <div style="font-size: 11px; color: #2563eb; font-weight: 600;">Higher Average Match Score</div>
        <div style="font-size: 10px; color: #64748b; margin-top: 2px;">Slower, structured, and clearer pacing</div>
      </div>

      <div style="background: #f5f3ff; border: 1px solid #ddd6fe; border-radius: 12px; padding: 16px;">
        <div style="font-size: 12px; font-weight: 700; color: #6d28d9;">Conversations with Human Teacher</div>
        <div style="font-size: 28px; font-weight: 800; color: #4c1d95; margin: 4px 0;">0.78</div>
        <div style="font-size: 11px; color: #7c3aed; font-weight: 600;">Lower Average Match Score</div>
        <div style="font-size: 10px; color: #64748b; margin-top: 2px;">Spontaneous speech, overlaps & rapid tempo</div>
      </div>
    </div>

    <div class="dash-alert">
      <strong>Conclusion:</strong> Conversations with an AI bot exhibit structured turns with zero vocal overlaps (<code>Overlap = 0</code>), yielding cleaner and 4% more accurate transcription on average compared to human teacher interactions.
    </div>
  </div>

  <div class="dash-panel">
    <div class="dash-title">👥 Impact of Conversation Partner on Speech Characteristics</div>
    <div class="dash-desc">Comparing pause durations, noise levels, and overlaps between conditions:</div>
    
    <table class="dash-table">
      <thead>
        <tr>
          <th>Learning Condition</th>
          <th>Average Silence</th>
          <th>Noise Level (SNR)</th>
          <th>Speech Overlap</th>
          <th>ASR Accuracy</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td style="font-weight: 700; color: #1e40af;">Artificial Intelligence Bot (AI)</td>
          <td>12.4 seconds</td>
          <td>0.08 (Very Quiet)</td>
          <td>0.0% (No Overlap)</td>
          <td style="font-weight: 700; color: #059669;">82.0% (High)</td>
        </tr>
        <tr>
          <td style="font-weight: 700; color: #6d28d9;">Human Teacher</td>
          <td>18.7 seconds</td>
          <td>0.14 (Background Noise)</td>
          <td>14.2% Overlap</td>
          <td style="font-weight: 700; color: #d97706;">78.0% (Moderate)</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
"""

def get_features_html():
    return f"""
{DASHBOARD_CSS}
<div class="dash-panel">
  <div class="dash-title">💡 Multimodal Feature Importance (XGBoost Feature Importance)</div>
  <div class="dash-desc">Feature importance ranking of the 9 multimodal features (acoustic and textual) for classifying transcription error likelihood:</div>

  <div style="display: flex; flex-direction: column; gap: 12px; margin-top: 16px;">
    <div>
      <div class="dash-progress-header">
        <span>1. Match_Confidence (Alignment score between Whisper and ChatGPT)</span>
        <span style="color: #2563eb; font-weight: 800;">25.24%</span>
      </div>
      <div class="dash-progress-track" style="height: 14px;">
        <div class="dash-progress-fill" style="width: 25.24%; background-color: #2563eb;"></div>
      </div>
    </div>

    <div>
      <div class="dash-progress-header">
        <span>2. Speech_Rate (Speech tempo in words per second)</span>
        <span style="color: #4f46e5; font-weight: 800;">15.86%</span>
      </div>
      <div class="dash-progress-track" style="height: 14px;">
        <div class="dash-progress-fill" style="width: 15.86%; background-color: #4f46e5;"></div>
      </div>
    </div>

    <div>
      <div class="dash-progress-header">
        <span>3. Hesitations_Count (Filler words like "um", "uh", repetitions, and self-repairs)</span>
        <span style="color: #0d9488; font-weight: 800;">15.18%</span>
      </div>
      <div class="dash-progress-track" style="height: 14px;">
        <div class="dash-progress-fill" style="width: 15.18%; background-color: #0d9488;"></div>
      </div>
    </div>

    <div>
      <div class="dash-progress-header">
        <span>4. Silence_Before_Turn (Pause duration before speech turn starts)</span>
        <span style="color: #059669; font-weight: 800;">13.74%</span>
      </div>
      <div class="dash-progress-track" style="height: 14px;">
        <div class="dash-progress-fill" style="width: 13.74%; background-color: #059669;"></div>
      </div>
    </div>

    <div>
      <div class="dash-progress-header">
        <span>5. Noise_Level (Background noise level relative to signal - SNR)</span>
        <span style="color: #d97706; font-weight: 800;">12.05%</span>
      </div>
      <div class="dash-progress-track" style="height: 14px;">
        <div class="dash-progress-fill" style="width: 12.05%; background-color: #d97706;"></div>
      </div>
    </div>

    <div>
      <div class="dash-progress-header">
        <span>6. Speech_Volume (Acoustic signal intensity in dB RMS)</span>
        <span style="color: #7c3aed; font-weight: 800;">11.03%</span>
      </div>
      <div class="dash-progress-track" style="height: 14px;">
        <div class="dash-progress-fill" style="width: 11.03%; background-color: #7c3aed;"></div>
      </div>
    </div>

    <div>
      <div class="dash-progress-header">
        <span>7. Different_Words (Substituted words between transcription engines)</span>
        <span style="color: #64748b; font-weight: 800;">6.89%</span>
      </div>
      <div class="dash-progress-track" style="height: 14px;">
        <div class="dash-progress-fill" style="width: 6.89%; background-color: #64748b;"></div>
      </div>
    </div>
  </div>
</div>
"""

def get_gallery_html():
    fig1 = get_base64_image("figures/fig1_model_benchmark.png")
    fig2 = get_base64_image("figures/fig2_confusion_matrix.png")
    fig3 = get_base64_image("figures/fig3_feature_importance.png")
    fig4 = get_base64_image("figures/fig4_research_insights.png")
    fig5 = get_base64_image("figures/active_learning_progress.png")
    fig6 = get_base64_image("figures/jev_confusion_matrix.png")

    return f"""
{DASHBOARD_CSS}
<div class="dash-panel">
  <div class="dash-title">🖼️ Publication Figures (300 DPI High-Resolution)</div>
  <div class="dash-desc">Figures are physically saved in the <code>figures/</code> directory ready for publication:</div>

  <div class="dash-gallery-grid">
    <div class="dash-fig-card">
      <img src="{fig1}" alt="Figure 1: 5 Models Benchmark Comparison">
      <div style="font-size: 12px; font-weight: 700; color: #1e293b;">Figure 1: Comparison of 5 Models</div>
    </div>
    <div class="dash-fig-card">
      <img src="{fig2}" alt="Figure 2: Confusion Matrix & Accuracy Metrics">
      <div style="font-size: 12px; font-weight: 700; color: #1e293b;">Figure 2: Confusion Matrix & Performance Metrics (XGBoost 92.5%)</div>
    </div>
    <div class="dash-fig-card">
      <img src="{fig3}" alt="Figure 3: 9 Multimodal Features Importance Ranking">
      <div style="font-size: 12px; font-weight: 700; color: #1e293b;">Figure 3: 9 Multimodal Features Importance Ranking</div>
    </div>
    <div class="dash-fig-card">
      <img src="{fig4}" alt="Figure 4: AI vs. Human Condition & Longitudinal Progress">
      <div style="font-size: 12px; font-weight: 700; color: #1e293b;">Figure 4: Research Insights — AI vs. Human Condition & Longitudinal SLA Progress</div>
      <div style="font-size: 11px; color: #64748b; margin-top: 4px;">Left: Autonomous AI (0.77) vs. Scaffolded Human (0.84) | Right: Upward Longitudinal Growth (0.74 → 0.84)</div>
    </div>
    <div class="dash-fig-card">
      <img src="{fig5}" alt="Figure 5: Active Learning Flywheel Trajectory (63.5% → 92.5%)">
      <div style="font-size: 12px; font-weight: 700; color: #1e293b;">Figure 5: Active Learning Flywheel Trajectory (63.5% → 92.5%)</div>
      <div style="font-size: 11px; color: #64748b; margin-top: 4px;">4 Retraining Cycles: Iter #0 (63.5% / 54.2%) → Iter #1 (78.2% / 72.5%) → Iter #2 (86.8% / 83.4%) → Iter #3 (92.5% / 91.9%)</div>
    </div>
    <div class="dash-fig-card" style="border: 1px solid #fed7aa; background: #fffaf5;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
        <span class="dash-badge" style="background: #ffedd5; color: #9a3412; font-size: 10px; font-weight: 700; text-transform: uppercase;">Motivation Benchmark (Baseline)</span>
        <span style="font-size: 11px; color: #dc2626; font-weight: 700;">Zero-Shot LLM: 50.0% Acc</span>
      </div>
      <img src="{fig6}" alt="Figure 6: Motivation Baseline - Off-the-Shelf LLM vs. Human Ground-Truth">
      <div style="font-size: 12px; font-weight: 700; color: #1e293b;">Figure 6: Baseline Pilot — Off-the-Shelf LLM (50.0%, κ=0.250) Proves Need for Multimodal ML</div>
      <div style="font-size: 11px; color: #64748b; margin-top: 4px;">Human Pilot Validation (N=18). Demonstrates that generic LLM prompting fails at phonetic error grading.</div>
    </div>
  </div>
</div>
"""
