import os
import gradio as gr
import pandas as pd
import librosa
import soundfile as sf
import re
import gradio.processing_utils as pu
pu.audio_is_playable = lambda *args, **kwargs: True


print("Loading database and initializing Gradio Tagging Interface... ⏳")

df_path = 'Transcripts/Final_Master_Database.xlsx'
audio_base_dir = 'Audio/'
df = pd.read_excel(df_path)

if 'Human_Label' not in df.columns:
    df['Human_Label'] = None

current_audio_name = None
y, sr = None, None

def safe_str(val):
    if pd.isna(val):
        return ""
    # If it's a float that is actually an int (e.g. 1.0), convert to int first
    if isinstance(val, float) and val.is_integer():
        return str(int(val))
    return str(val).strip()

def get_row_data(idx):
    global current_audio_name, y, sr
    try:
        idx = max(0, min(len(df) - 1, int(idx)))
        row = df.iloc[idx]
        chat_text = str(row.get('ChatGPT Transcript', ''))
        whisp_text = str(row.get('Additional ASR Transcript', ''))
        
        start = row.get('Start Time')
        end = row.get('End Time')

        cond_col = next((c for c in df.columns if "condition" in c.lower()), "Condition: AI \u05d0\u05d5 Human")
        condition = safe_str(row.get(cond_col, 'AI'))
        if condition == "":
            condition = "AI"
            
        student_id = safe_str(row.get('Student ID', ''))
        session_num = safe_str(row.get('Session Number', ''))
        
        expected_audio_name = f"{condition}_{student_id}_{session_num}_audio.m4a"

        # Load audio only when recording changes to maximize efficiency
        if current_audio_name != expected_audio_name:
            audio_path = os.path.join(audio_base_dir, expected_audio_name)
            if os.path.exists(audio_path):
                y, sr = librosa.load(audio_path, sr=None)
                current_audio_name = expected_audio_name
            else:
                found = False
                if os.path.exists(audio_base_dir):
                    for f in os.listdir(audio_base_dir):
                        if f.endswith('.m4a') and condition in f and student_id in f and session_num in f:
                            audio_path = os.path.join(audio_base_dir, f)
                            y, sr = librosa.load(audio_path, sr=None)
                            current_audio_name = expected_audio_name
                            found = True
                            break
                if not found:
                    return f"Audio file not found: {expected_audio_name}", "", None, f"Row {idx + 1} of {len(df)}", f"Missing file: {expected_audio_name}", "No audio", "⚪ Audio Missing", idx + 1, idx

        temp_path = None
        if pd.notna(start) and pd.notna(end) and start < end and y is not None:
            start_idx = max(0, int(start * sr))
            end_idx = min(len(y), int(end * sr))
            chunk = y[start_idx:end_idx]
            
            import tempfile
            local_tmp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio_chunks")
            os.makedirs(local_tmp, exist_ok=True)
            
            fd, temp_path = tempfile.mkstemp(suffix=".wav", dir=local_tmp)
            os.close(fd)
            sf.write(temp_path, chunk, sr)

        # Extract Jev AI decision parameters
        jev_conf = row.get('Jev_Confidence')
        jev_pred = row.get('Jev_Predicted_Category')
        status = str(row.get('Label_Status', ''))

        if pd.notna(jev_conf):
            conf_pct = int(jev_conf * 100) if jev_conf <= 1.0 else int(jev_conf)
            if conf_pct >= 70:
                jev_info = f"🤖 Jev AI: {jev_pred} | 🟢 High Confidence: {conf_pct}% ({status})"
            else:
                jev_info = f"🤖 Jev AI: {jev_pred} | ⚠️ Borderline / Low Confidence: {conf_pct}% (Human Review Required)"
        else:
            jev_info = "🤖 Jev AI: Not evaluated yet"

        # Current Saved Label
        curr_lbl = row.get('Human_Label')
        curr_stat = row.get('Label_Status')
        if pd.isna(curr_lbl) or str(curr_lbl).strip() == "" or str(curr_lbl).lower() == "nan":
            curr_label_str = "⚪ Unlabeled"
        else:
            stat_str = f" [{curr_stat}]" if pd.notna(curr_stat) and str(curr_stat) != 'nan' else ""
            curr_label_str = f"🏷️ {curr_lbl}{stat_str}"

        # Grammatically Corrected Sentence
        corr_sent = str(row.get('Corrected Sentence', ''))
        if corr_sent == 'nan':
            corr_sent = ''

        prog_info = f"Row {idx + 1} of {len(df)} ({((idx + 1) / len(df) * 100):.1f}%) | Verified: {df['Human_Label'].notna().sum()}"
        rec_info = f"👤 Student: {student_id} | 📅 Session {session_num} | Partner: {condition}"

        return chat_text, whisp_text, temp_path, prog_info, rec_info, jev_info, curr_label_str, corr_sent, idx + 1, idx
    except Exception as e:
        return f"Error loading data: {str(e)}", "", None, "Error", f"Exception at index {idx}", "Error", "Error", "", idx + 1, idx

def go_prev(idx):
    new_idx = max(0, int(idx) - 1)
    return get_row_data(new_idx)

def go_next(idx):
    new_idx = min(len(df) - 1, int(idx) + 1)
    return get_row_data(new_idx)

def jump_to_row(row_val):
    try:
        target = max(0, min(len(df) - 1, int(row_val) - 1))
    except Exception:
        target = 0
    return get_row_data(target)

def label_and_advance(label, idx, edited_correction):
    if 0 <= idx < len(df):
        df.at[idx, 'Human_Label'] = label
        df.at[idx, 'Label_Status'] = 'Human_Reviewed'
        if edited_correction is not None and str(edited_correction).strip() != "":
            df.at[idx, 'Corrected Sentence'] = str(edited_correction).strip()
        try:
            df.to_excel(df_path, index=False)
        except Exception as e:
            print(f"Error saving to excel: {e}")
    next_idx = min(len(df) - 1, int(idx) + 1)
    return get_row_data(next_idx)

def save_correction_only(idx, edited_correction):
    if 0 <= idx < len(df):
        if edited_correction is not None:
            df.at[idx, 'Corrected Sentence'] = str(edited_correction).strip()
        try:
            df.to_excel(df_path, index=False)
        except Exception as e:
            print(f"Error saving to excel: {e}")
    return get_row_data(idx)

import html

custom_css = """
#tagging-tab {
    direction: ltr !important;
    text-align: left !important;
}
#tagging-tab * {
    direction: ltr !important;
}
#dashboard-tab {
    direction: ltr !important;
    text-align: left !important;
    padding: 0 !important;
}
"""

with gr.Blocks(title="English Speech Quality System & Analytics Dashboard") as app:
    with gr.Tabs():
        with gr.Tab("🎧 Ground-Truth Annotation", elem_id="tagging-tab"):
            gr.Markdown("## 🎧 Ground-Truth Annotation & Audio Inspection System")

            # Determine starting row: first unlabeled row if any, else 0
            unlabeled = df[df['Human_Label'].isna()]
            start_idx = int(unlabeled.index[0]) if not unlabeled.empty else 0
            idx_state = gr.State(value=start_idx)

            # --- Row 1: Navigation Controls (Prev / Jump / Next) ---
            with gr.Row():
                btn_prev = gr.Button("⬅️ Previous Row", variant="secondary", scale=2)
                row_num_input = gr.Number(label="Go to Row #", value=start_idx + 1, precision=0, minimum=1, maximum=len(df), scale=1)
                btn_jump = gr.Button("Jump 🔍", scale=1)
                btn_next = gr.Button("➡️ Next Row", variant="secondary", scale=2)

            # --- Row 2: Status, Metadata & Current Saved Label ---
            with gr.Row():
                file_info = gr.Textbox(label="Recording Metadata", interactive=False, scale=2)
                prog_text = gr.Textbox(label="Overall Progress", interactive=False, scale=2)
                current_label_box = gr.Textbox(label="🏷️ Current Saved Label", interactive=False, scale=2)

            # --- Row 3: Synchronized Audio ---
            with gr.Row():
                audio_player = gr.Audio(label="Synchronized Audio Segment", type="filepath")

            # --- Row 4: Side-by-Side Transcripts ---
            with gr.Row():
                chatgpt_box = gr.Textbox(label="ChatGPT Transcript", interactive=False, lines=3)
                whisper_box = gr.Textbox(label="Acoustic Whisper Transcript", interactive=False, lines=3)

            # --- Row 5: Grammatically Corrected Sentence (Editable) ---
            with gr.Row():
                corrected_box = gr.Textbox(
                    label="✍️ Grammatically Corrected Sentence (Editable)",
                    placeholder="Enter or refine the grammatically corrected version of the student utterance...",
                    lines=2,
                    interactive=True
                )

            # --- Row 6: Jev AI Assistant Suggestions ---
            with gr.Row():
                jev_box = gr.Textbox(label="🤖 Jev AI Assistant (Confidence & Suggested Categorization)", interactive=False)

            # --- Row 7: Annotation Decision Buttons (Fix / Overwrite anytime) ---
            with gr.Row():
                btn_good = gr.Button("Valid ✅", variant="primary", scale=2)
                btn_minor = gr.Button("Minor Correction ⚠️", variant="secondary", scale=2)
                btn_major = gr.Button("Major Correction ❌", variant="stop", scale=2)
                btn_save_corr = gr.Button("💾 Save Correction Only", scale=1)

            # --- Row 8: Active Learning Flywheel ---
            with gr.Accordion("🔄 Active Learning Flywheel: Continuous Model Retraining", open=False):
                with gr.Row():
                    flywheel_status = gr.Textbox(
                        label="Quality Estimator Model Status",
                        value=f"🏆 Model: XGBoost | Pool: {df['Human_Label'].notna().sum()} Verified Turns | Binary Accuracy: 92.5%",
                        interactive=False
                    )
                    retrain_btn = gr.Button("🚀 Retrain Model on Verified Data", variant="secondary")
                retrain_feedback = gr.Markdown("💡 *Click 'Retrain Model' after reviewing deferred cases to update decision boundaries and sharpen accuracy.*")

                def handle_retrain():
                    from train_flywheel import retrain_active_learning
                    res = retrain_active_learning(verbose=False)
                    if res.get("status") == "success":
                        new_status = f"🏆 Model: XGBoost (Iter #{res['iteration']}) | Pool: {res['samples']} Turns | Accuracy: {res['binary_accuracy']*100:.1f}% (F1: {res['binary_f1']*100:.1f}%)"
                        msg = f"✅ **Retrained Successfully!** Model updated across {res['samples']} verified samples.\n- **Binary Accuracy**: {res['binary_accuracy']*100:.2f}% (F1: {res['binary_f1']*100:.2f}%)\n- **3-Class Accuracy**: {res['3class_accuracy']*100:.2f}% (F1: {res['3class_f1_macro']*100:.2f}%)\n- Model artifacts saved to `models/`."
                        return new_status, msg
                    else:
                        return "⚠️ Retraining Failed", f"❌ Error: {res.get('message')}"

                retrain_btn.click(handle_retrain, outputs=[flywheel_status, retrain_feedback])

            # Output components bundle
            ui_outputs = [
                chatgpt_box,
                whisper_box,
                audio_player,
                prog_text,
                file_info,
                jev_box,
                current_label_box,
                corrected_box,
                row_num_input,
                idx_state
            ]

            # Connect event listeners
            app.load(lambda: get_row_data(start_idx), outputs=ui_outputs)
            btn_prev.click(go_prev, inputs=[idx_state], outputs=ui_outputs)
            btn_next.click(go_next, inputs=[idx_state], outputs=ui_outputs)
            btn_jump.click(jump_to_row, inputs=[row_num_input], outputs=ui_outputs)
            row_num_input.submit(jump_to_row, inputs=[row_num_input], outputs=ui_outputs)

            btn_good.click(lambda i, c: label_and_advance("Valid", i, c), inputs=[idx_state, corrected_box], outputs=ui_outputs)
            btn_minor.click(lambda i, c: label_and_advance("Minor Correction", i, c), inputs=[idx_state, corrected_box], outputs=ui_outputs)
            btn_major.click(lambda i, c: label_and_advance("Major Correction", i, c), inputs=[idx_state, corrected_box], outputs=ui_outputs)
            btn_save_corr.click(save_correction_only, inputs=[idx_state, corrected_box], outputs=ui_outputs)


        with gr.Tab("📊 Research Analytics & Statistics Dashboard", elem_id="dashboard-tab"):
            dashboard_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard.html")
            dash_content = ""
            if os.path.exists(dashboard_path):
                with open(dashboard_path, "r", encoding="utf-8") as f:
                    dash_content = f.read()
            escaped_dash = html.escape(dash_content, quote=True)
            gr.HTML(f'<iframe srcdoc="{escaped_dash}" style="width: 100%; min-height: 1400px; height: 100vh; border: none; border-radius: 16px; background-color: #f8fafc;" frameborder="0"></iframe>')


if __name__ == "__main__":
    app.launch(server_name="127.0.0.1", server_port=7860, debug=True, css=custom_css, head=f"<style>{custom_css}</style>")

