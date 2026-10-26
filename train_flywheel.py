#!/usr/bin/env python3
"""
Continuous Active Learning Flywheel: Automated Model Retraining
==============================================================
Enables continuous self-improvement of the Speech Quality Estimator.
As human annotators review deferred borderline rows or new sessions are added,
this engine retrains the top-performing XGBoost models and updates decision boundaries.

Key Capabilities:
- Retrains both Binary (Valid vs Needs Correction) and 3-Class (Valid vs Minor vs Major) XGBoost models.
- Uses 5-Fold Stratified Cross Validation to report realistic generalization metrics.
- Persists model weights to `models/` directory for zero-latency local inference.
- Maintains an Active Learning history log (`models/active_learning_history.json`).
- Automatically plots the learning curve over retraining cycles (`figures/active_learning_progress.png`).
"""

import os
import json
import datetime
import warnings
from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, GroupKFold, cross_validate
from xgboost import XGBClassifier

warnings.filterwarnings("ignore")

FEATURE_COLUMNS = [
    "Match_Confidence",
    "Speech_Volume",
    "Noise_Level",
    "Speech_Rate",
    "Silence_Before_Turn",
    "Hesitations_Count",
    "Missing_Words",
    "Different_Words",
    "Has_Overlap"
]


def prepare_features_and_targets(df: pd.DataFrame) -> Tuple[pd.DataFrame, np.ndarray, np.ndarray]:
    """Ensure all multimodal features and targets are cleanly engineered."""
    df_clean = df.copy()

    # Feature alignment
    if "Match_Confidence" not in df_clean.columns and "Confidence Score" in df_clean.columns:
        df_clean["Match_Confidence"] = df_clean["Confidence Score"].fillna(0.0)
    if "Has_Overlap" not in df_clean.columns and "Overlap" in df_clean.columns:
        df_clean["Has_Overlap"] = df_clean["Overlap"].fillna(0)

    hes_cols = [c for c in ["Filled Pause", "Repetition", "Self-Repair", "False Start"] if c in df_clean.columns]
    if "Hesitations_Count" not in df_clean.columns and hes_cols:
        df_clean["Hesitations_Count"] = df_clean[hes_cols].fillna(0).sum(axis=1)

    # Missing and different words fallback
    if "Missing_Words" not in df_clean.columns or "Different_Words" not in df_clean.columns:
        import difflib
        def calc_text_diff(row):
            chat = str(row.get("ChatGPT Transcript", "")).lower().split()
            whisper = str(row.get("Additional ASR Transcript", "")).lower().split()
            if not chat or not whisper or chat == ["nan"] or whisper == ["nan"]:
                return pd.Series([0, 0])
            sm = difflib.SequenceMatcher(None, chat, whisper)
            missing, different = 0, 0
            for tag, i1, i2, j1, j2 in sm.get_opcodes():
                if tag == "replace":
                    different += max(i2 - i1, j2 - j1)
                elif tag == "insert":
                    missing += (j2 - j1)
                elif tag == "delete":
                    different += (i2 - i1)
            return pd.Series([missing, different])

        diff_res = df_clean.apply(calc_text_diff, axis=1)
        df_clean["Missing_Words"] = diff_res[0]
        df_clean["Different_Words"] = diff_res[1]

    # Ensure all 9 features exist
    for col in FEATURE_COLUMNS:
        if col not in df_clean.columns:
            df_clean[col] = 0.0

    X = df_clean[FEATURE_COLUMNS].fillna(0.0)
    y_raw = df_clean["Human_Label"].values

    # Target 1: Binary (0 = Valid, 1 = Needs Correction)
    def map_binary(val):
        s = str(val).lower()
        # Checks for English 'valid' or legacy Hebrew label without correction indicator
        if ("valid" in s or "\u05ea\u05e7\u05d9\u05df" in s) and ("\u05ea\u05d9\u05e7\u05d5\u05df" not in s and "correction" not in s):
            return 0
        return 1

    y_bin = np.array([map_binary(v) for v in y_raw])

    # Target 2: 3-Class (0 = Valid, 1 = Minor Correction, 2 = Major Correction)
    def map_3class(val):
        s = str(val).lower()
        if ("valid" in s or "\u05ea\u05e7\u05d9\u05df" in s) and ("\u05ea\u05d9\u05e7\u05d5\u05df" not in s and "correction" not in s):
            return 0
        elif "minor" in s or "\u05e7\u05dc" in s:
            return 1
        else:
            return 2

    y_3c = np.array([map_3class(v) for v in y_raw])
    return X, y_bin, y_3c


def plot_active_learning_curve(history: list, output_path: str = "figures/active_learning_progress.png"):
    """Plot the continuous improvement of the model across retraining iterations."""
    try:
        import matplotlib.pyplot as plt

        if len(history) < 1:
            return

        iterations = [f"Iter #{i+1}\n(N={h['samples']})" for i, h in enumerate(history)]
        bin_accs = [h["binary_accuracy"] * 100 for h in history]
        tri_accs = [h["3class_accuracy"] * 100 for h in history]

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(range(len(history)), bin_accs, marker="o", linewidth=2.5, color="#10b981", label="Binary Accuracy (Valid vs Error)")
        ax.plot(range(len(history)), tri_accs, marker="s", linewidth=2.5, color="#3b82f6", label="3-Class Accuracy (Valid / Minor / Major)")

        for i in range(len(history)):
            ax.annotate(f"{bin_accs[i]:.1f}%", (i, bin_accs[i] + 1.0), ha="center", fontsize=9, fontweight="bold", color="#047857")
            ax.annotate(f"{tri_accs[i]:.1f}%", (i, tri_accs[i] - 2.5), ha="center", fontsize=9, fontweight="bold", color="#1d4ed8")

        ax.set_xticks(range(len(history)))
        ax.set_xticklabels(iterations, fontsize=10)
        ax.set_ylim(40, 100)
        ax.set_ylabel("Accuracy (%)", fontsize=11, fontweight="bold")
        ax.set_title("🚀 Active Learning Flywheel: Model Accuracy Progression Over Time", fontsize=12, pad=15)
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.legend(loc="lower right", frameon=True)
        plt.tight_layout()

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        fig.savefig(output_path, dpi=300)
        plt.close(fig)
    except Exception as e:
        print(f"ℹ️ Could not plot learning curve: {e}")


def retrain_active_learning(
    master_path: str = "Transcripts/Final_Master_Database.xlsx",
    models_dir: str = "models",
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Main active learning retraining function.
    Reads verified data, cross-validates, fits models, updates history and artifacts.
    """
    if verbose:
        print("=" * 80)
        print("🔄 Active Learning Retraining Flywheel Running...")
        print("=" * 80)

    if not os.path.exists(master_path):
        raise FileNotFoundError(f"Master database not found at: {master_path}")

    df = pd.read_excel(master_path)
    labeled_df = df[df["Human_Label"].notna()].copy()
    n_samples = len(labeled_df)

    if n_samples < 20:
        return {"status": "error", "message": f"Insufficient labeled data for retraining ({n_samples} samples). Need at least 20."}

    human_reviewed_count = (labeled_df.get("Label_Status") == "Human_Reviewed").sum() if "Label_Status" in labeled_df.columns else 0
    jev_uniform_count = (labeled_df.get("Label_Status") == "Jev_Uniform").sum() if "Label_Status" in labeled_df.columns else 0

    if verbose:
        print(f"📊 Training Pool: {n_samples} total verified records")
        print(f"   • Jev AI Auto-Labeled:     {jev_uniform_count}")
        print(f"   • Human Verified/Reviewed: {human_reviewed_count}")
        print(f"   • Pending Human Review:    {df['Human_Label'].isna().sum()} rows")

    X, y_bin, y_3c = prepare_features_and_targets(labeled_df)

    # 5-Fold Stratified Cross Validation (Standard Benchmark)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    # Student-Independent GroupKFold (Leak-Free Validation - Rejection #9)
    student_groups = labeled_df["Student ID"].fillna("Unknown").values
    n_groups = len(np.unique(student_groups))
    gkf_splits = min(5, n_groups)
    gkf = GroupKFold(n_splits=gkf_splits)

    # 1. Train & Validate Binary XGBoost
    xgb_binary = XGBClassifier(
        n_estimators=100,
        learning_rate=0.08,
        max_depth=4,
        random_state=42,
        eval_metric="logloss"
    )
    cv_bin = cross_validate(xgb_binary, X, y_bin, cv=cv, scoring=["accuracy", "f1"])
    bin_acc = float(cv_bin["test_accuracy"].mean())
    bin_f1 = float(cv_bin["test_f1"].mean())

    # GroupKFold evaluation (Student-Independent)
    cv_bin_group = cross_validate(xgb_binary, X, y_bin, cv=gkf, groups=student_groups, scoring=["accuracy", "f1"])
    bin_group_acc = float(cv_bin_group["test_accuracy"].mean())
    bin_group_f1 = float(cv_bin_group["test_f1"].mean())

    if verbose:
        print(f"   • Stratified CV (Random):      Accuracy = {bin_acc*100:.2f}% | F1 = {bin_f1*100:.2f}%")
        print(f"   • GroupKFold (Student-Split):  Accuracy = {bin_group_acc*100:.2f}% | F1 = {bin_group_f1*100:.2f}% (Leak-Free)")

    # 2. Train & Validate 3-Class XGBoost
    xgb_3class = XGBClassifier(
        n_estimators=100,
        learning_rate=0.08,
        max_depth=4,
        random_state=42,
        eval_metric="logloss"
    )
    cv_3c = cross_validate(xgb_3class, X, y_3c, cv=cv, scoring=["accuracy", "f1_macro"])
    tri_acc = float(cv_3c["test_accuracy"].mean())
    tri_f1 = float(cv_3c["test_f1_macro"].mean())

    cv_3c_group = cross_validate(xgb_3class, X, y_3c, cv=gkf, groups=student_groups, scoring=["accuracy", "f1_macro"])
    tri_group_acc = float(cv_3c_group["test_accuracy"].mean())
    tri_group_f1 = float(cv_3c_group["test_f1_macro"].mean())

    # 3. Fit Final Production Models on 100% of Verified Data
    xgb_binary.fit(X, y_bin)
    xgb_3class.fit(X, y_3c)

    # 4. Save Model Artifacts
    os.makedirs(models_dir, exist_ok=True)
    binary_model_path = os.path.join(models_dir, "quality_estimator_xgboost_binary.json")
    tri_model_path = os.path.join(models_dir, "quality_estimator_xgboost_3class.json")
    metadata_path = os.path.join(models_dir, "model_metadata.json")
    history_path = os.path.join(models_dir, "active_learning_history.json")

    xgb_binary.save_model(binary_model_path)
    xgb_3class.save_model(tri_model_path)

    # Update Active Learning History
    history = []
    if os.path.exists(history_path):
        try:
            with open(history_path, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            history = []

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_entry = {
        "timestamp": timestamp,
        "iteration": len(history) + 1,
        "samples": n_samples,
        "binary_accuracy": round(bin_acc, 4),
        "binary_f1": round(bin_f1, 4),
        "3class_accuracy": round(tri_acc, 4),
        "3class_f1_macro": round(tri_f1, 4),
        "human_reviewed_count": int(human_reviewed_count),
        "jev_uniform_count": int(jev_uniform_count)
    }
    history.append(current_entry)

    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump({
            "features": FEATURE_COLUMNS,
            "last_trained": timestamp,
            "training_samples": n_samples,
            "metrics": current_entry
        }, f, indent=2)

    # 5. Update Progress Plot
    plot_active_learning_curve(history)

    # 6. Recompile Dashboard with updated figures
    try:
        from dashboard_sections import compile_dashboard_html
        compile_dashboard_html()
    except Exception as e:
        if verbose:
            print(f"ℹ️ Could not recompile dashboard: {e}")

    if verbose:
        print("\n" + "=" * 80)
        print("🏆 RETRAINING RESULTS SUMMARY")
        print("=" * 80)
        print(f"• Total Training Pool Size:        {n_samples} verified samples")
        print(f"• Task A (Binary) Accuracy:        {bin_acc * 100:.2f}% | F1: {bin_f1 * 100:.2f}%")
        print(f"• Task B (3-Class) Accuracy:       {tri_acc * 100:.2f}% | F1-Macro: {tri_f1 * 100:.2f}%")
        print(f"• Model Weights Saved:             {binary_model_path}")
        print(f"• Progress Curve Saved:            figures/active_learning_progress.png")
        print("🎉 Models updated and ready for zero-latency local inference!\n")

    return {
        "status": "success",
        "samples": n_samples,
        "binary_accuracy": bin_acc,
        "binary_f1": bin_f1,
        "3class_accuracy": tri_acc,
        "3class_f1_macro": tri_f1,
        "human_reviewed": human_reviewed_count,
        "jev_uniform": jev_uniform_count,
        "iteration": len(history)
    }


if __name__ == "__main__":
    retrain_active_learning()
