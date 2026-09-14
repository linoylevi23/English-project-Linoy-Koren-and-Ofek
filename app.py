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
        if idx >= len(df):
            return "Tagging Completed!", "", None, "🎉 Project Finished!", "No more data"

        row = df.iloc[idx]
        chat_text = str(row.get('ChatGPT Transcript', ''))
        whisp_text = str(row.get('Additional ASR Transcript', ''))
        
        start = row.get('Start Time')
        end = row.get('End Time')

        condition = safe_str(row.get('Condition: AI או Human', 'AI'))
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
                # Look for matching pattern in case of minor naming differences
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
                    return f"Audio file not found: {expected_audio_name}", "", None, "Error", f"Missing file: {expected_audio_name}"

        temp_path = None
        if pd.notna(start) and pd.notna(end) and start < end and y is not None:
            # Ensure indices are within bounds
            start_idx = max(0, int(start * sr))
            end_idx = min(len(y), int(end * sr))
            chunk = y[start_idx:end_idx]
            
            # Use a local temp dir to bypass Gradio 'File not allowed' error
            import tempfile
            local_tmp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio_chunks")
            os.makedirs(local_tmp, exist_ok=True)
            
            fd, temp_path = tempfile.mkstemp(suffix=".wav", dir=local_tmp)
            os.close(fd)
            sf.write(temp_path, chunk, sr)

        return chat_text, whisp_text, temp_path, f"Row {idx + 1} of {len(df)}", f"👤 {student_id} | 📅 Session {session_num}"
    except Exception as e:
        return f"Error loading data: {str(e)}", "", None, "Error", f"Exception at index {idx}"

def label_and_next(label, idx):
    if idx < len(df):
        df.at[idx, 'Human_Label'] = label
        try:
            df.to_excel(df_path, index=False)
        except Exception as e:
            print(f"Error saving to excel: {e}")
    next_idx = idx + 1
    return get_row_data(next_idx) + (next_idx,)

with gr.Blocks(title="English Speech Quality System & Analytics Dashboard") as app:
    with gr.Tabs():
        with gr.Tab("🎧 Ground-Truth Annotation"):
            gr.Markdown("## 🎧 Ground-Truth Annotation & Audio Inspection System")

            start_idx = int(df['Human_Label'].isna().idxmax()) if df['Human_Label'].isna().any() else len(df)
            idx_state = gr.State(value=start_idx)

            with gr.Row():
                file_info = gr.Textbox(label="Recording Metadata", interactive=False)
                prog_text = gr.Textbox(label="Overall Progress", interactive=False)
            with gr.Row():
                audio_player = gr.Audio(label="Synchronized Audio Segment", type="filepath")
            with gr.Row():
                chatgpt_box = gr.Textbox(label="ChatGPT Transcript", interactive=False)
                whisper_box = gr.Textbox(label="Acoustic Whisper Transcript", interactive=False)
            with gr.Row():
                btn_good = gr.Button("Valid / תקין ✅", variant="primary")
                btn_minor = gr.Button("Minor Correction / נדרש תיקון קל ⚠️")
                btn_major = gr.Button("Major Correction / נדרש תיקון משמעותי ❌", variant="stop")

            app.load(get_row_data, inputs=[idx_state], outputs=[chatgpt_box, whisper_box, audio_player, prog_text, file_info])
            btn_good.click(lambda i: label_and_next("תקין", i), inputs=[idx_state], outputs=[chatgpt_box, whisper_box, audio_player, prog_text, file_info, idx_state])
            btn_minor.click(lambda i: label_and_next("נדרש תיקון קל", i), inputs=[idx_state], outputs=[chatgpt_box, whisper_box, audio_player, prog_text, file_info, idx_state])
            btn_major.click(lambda i: label_and_next("נדרש תיקון משמעותי", i), inputs=[idx_state], outputs=[chatgpt_box, whisper_box, audio_player, prog_text, file_info, idx_state])

        with gr.Tab("📊 Research Analytics & Statistics Dashboard"):
            dashboard_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard.html")
            dashboard_html = ""
            if os.path.exists(dashboard_path):
                with open(dashboard_path, "r", encoding="utf-8") as f:
                    dashboard_html = f.read()
            gr.HTML(dashboard_html)


if __name__ == "__main__":
    app.launch(server_name="127.0.0.1", server_port=7860, debug=True)
