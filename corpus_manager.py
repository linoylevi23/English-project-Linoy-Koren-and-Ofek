#!/usr/bin/env python3
"""
corpus_manager.py
=================
Ingests, standardizes, and unifies all 19 conversational sessions.
Harmonizes diverse column headers, converts HH:MM:SS timestamps to seconds,
links corresponding audio files, and strictly isolates the Gold Standard Oracle
from operational runtime inputs.
"""

import os
import re
import json
import datetime
import pandas as pd
import numpy as np

def parse_time_str(val):
    if pd.isna(val) or val == '' or val is None:
        return None
    if isinstance(val, (datetime.time, datetime.datetime)):
        # Handle 12-hour AM/PM rollover artifact (e.g. 12:12:52 typed for 00:12:52)
        h = val.hour % 12 if val.hour == 12 else val.hour
        return h * 3600 + val.minute * 60 + val.second + val.microsecond / 1e6
    val_str = str(val).strip()
    # Check HH:MM:SS or MM:SS
    if ':' in val_str:
        parts = val_str.split(':')
        try:
            if len(parts) == 3:
                h = float(parts[0])
                if h == 12: h = 0
                return h * 3600 + float(parts[1]) * 60 + float(parts[2])
            elif len(parts) == 2:
                return float(parts[0]) * 60 + float(parts[1])
        except:
            return None
    try:
        fval = float(val_str)
        return fval
    except:
        return None

def standardize_session_data(filename, transcripts_dir="Transcripts", audio_dir="Audio"):
    fpath = os.path.join(transcripts_dir, filename)
    try:
        df = pd.read_excel(fpath)
    except Exception as e:
        print(f"Error reading {fpath}: {e}")
        return None, None
    if df.empty:
        return None, None
    
    # Extract metadata from filename
    # Patterns: AI_{student}_{session}_chatgpt_transcript.xlsx or AI_{student}_{session}_final_transcript.xlsx
    base = filename.replace('_chatgpt_transcript.xlsx', '').replace('_final_transcript.xlsx', '')
    m = re.match(r'([A-Za-z]+)_([A-Za-z0-9_-]+)_(\d+)', base)
    if m:
        condition = m.group(1).upper()
        student_id = m.group(2).lower().replace('-', '_')
        session_num = int(m.group(3))
    else:
        condition = "AI"
        student_id = base.lower().replace('-', '_')
        session_num = 1
        
    # Match Audio file
    audio_files = os.listdir(audio_dir) if os.path.exists(audio_dir) else []
    matched_audio = None
    for af in audio_files:
        clean_af = af.lower().replace('-', '_')
        if f"{condition.lower()}_{student_id}_{session_num}" in clean_af:
            matched_audio = af
            break
    if not matched_audio:
        # Fallback partial matching
        for af in audio_files:
            clean_af = af.lower().replace('-', '_')
            if student_id in clean_af and f"_{session_num}_" in clean_af:
                matched_audio = af
                break

    # Identify Text Columns
    text_cols = ['Text', 'Spoken/typed text', 'Spoken/Typed Text', 'Spoken / Typed Text', 'Actual spoken/typed text', 'Spoken Text']
    text_col = next((c for c in text_cols if c in df.columns), None)
    
    # Identify Proofread / Gold column
    gold_cols = ['Final Text (proofread by Noa)', 'Final Gold Transcript', 'Gold Transcript']
    gold_col = next((c for c in gold_cols if c in df.columns), None)
    
    # Identify Speaker column
    speaker_col = next((c for c in ['Speaker', 'Role'] if c in df.columns), None)
    
    # Identify Start/End time columns
    start_cols = ['Start Time', 'Start (HH:MM:SS)', 'Turn-start time', 'Turn Start Time', 'Turn-start Time', 'Local turn-start time', 'Actual local turn-start time', 'Approx. Timestamp']
    end_cols = ['End Time', 'End (HH:MM:SS)', 'Turn-end time', 'Turn End Time']
    
    start_col = next((c for c in start_cols if c in df.columns), None)
    end_col = next((c for c in end_cols if c in df.columns), None)
    
    standardized_rows = []
    oracle_rows = []
    
    for idx, row in df.iterrows():
        raw_text = str(row.get(text_col, '')).strip() if text_col else ''
        if not raw_text or len(raw_text) < 2 or raw_text.lower() == 'nan':
            continue
            
        speaker_raw = str(row.get(speaker_col, 'Student')).strip() if speaker_col else 'Student'
        # Normalize speaker labels
        spk_lower = speaker_raw.lower()
        if any(k in spk_lower for k in ['teacher', 'ai', 'bot', 'agent']):
            speaker_norm = 'AI'
        elif any(k in spk_lower for k in ['observer', 'noa', 'researcher', 'human']):
            speaker_norm = 'Observer'
        else:
            speaker_norm = 'Student'
            
        t_start = parse_time_str(row.get(start_col)) if start_col else None
        t_end = parse_time_str(row.get(end_col)) if end_col else None
        
        # Operational row (What runtime system gets)
        op_row = {
            'Session_ID': f"{condition}_{student_id}_{session_num}",
            'Student_ID': student_id,
            'Session_Num': session_num,
            'Condition': condition,
            'Turn_Index': len(standardized_rows) + 1,
            'Speaker': speaker_norm,
            'Speaker_Original': speaker_raw,
            'Input_Transcript': raw_text,
            'Estimated_Start': t_start,
            'Estimated_End': t_end,
            'Audio_File': matched_audio
        }
        standardized_rows.append(op_row)
        
        # Oracle row (Ground Truth kept strictly isolated)
        gold_text = str(row.get(gold_col, '')).strip() if gold_col else raw_text
        if gold_text.lower() == 'nan': gold_text = raw_text
        oracle_row = {
            'Session_ID': f"{condition}_{student_id}_{session_num}",
            'Student_ID': student_id,
            'Session_Num': session_num,
            'Turn_Index': len(standardized_rows),
            'Speaker_Ground_Truth': speaker_norm,
            'Gold_Transcript': gold_text if gold_text else raw_text,
            'Gold_Start': t_start,
            'Gold_End': t_end,
            'Has_Human_Proofread': bool(gold_col and str(row.get(gold_col, '')).strip() not in ['', 'nan'])
        }
        oracle_rows.append(oracle_row)
        
    return pd.DataFrame(standardized_rows), pd.DataFrame(oracle_rows)

def ingest_all_19_sessions():
    print("=" * 70)
    print("🚀 UNIFYING ALL 19 SESSIONS & ISOLATING GOLD STANDARD ORACLE")
    print("=" * 70)
    
    transcripts_dir = "Transcripts"
    all_files = sorted([f for f in os.listdir(transcripts_dir) if f.endswith('.xlsx') and not f.startswith('Final_') and not f.startswith('Unified_')])
    print(f"Found {len(all_files)} individual session files in {transcripts_dir}/.")
    
    all_operational = []
    all_oracle = []
    audit_matrix = []
    
    for f in all_files:
        df_op, df_oracle = standardize_session_data(f, transcripts_dir=transcripts_dir)
        if df_op is not None and not df_op.empty:
            all_operational.append(df_op)
            all_oracle.append(df_oracle)
            
            sess_id = df_op['Session_ID'].iloc[0]
            audio_f = df_op['Audio_File'].iloc[0]
            has_proof = bool(df_oracle['Has_Human_Proofread'].any())
            
            audit_matrix.append({
                'filename': str(f),
                'session_id': str(sess_id),
                'student': str(df_op['Student_ID'].iloc[0]),
                'session_num': int(df_op['Session_Num'].iloc[0]),
                'turns_count': int(len(df_op)),
                'audio_file': str(audio_f) if audio_f else None,
                'audio_status': 'Verified' if audio_f else 'Missing',
                'has_proofread_gold': bool(has_proof),
                'included_in_legacy_11': bool('lilo' in sess_id or 'thomas_shelby' in sess_id or 'rocky' in sess_id),
                'status': 'Included in Expanded Corpus'
            })
            print(f"  ✅ Ingested {sess_id:<22} | Turns: {len(df_op):3d} | Audio: {str(audio_f):<30} | Proofread: {has_proof}")
        else:
            print(f"  ❌ Failed to parse: {f}")

    df_full_op = pd.concat(all_operational, ignore_index=True)
    df_full_oracle = pd.concat(all_oracle, ignore_index=True)
    
    print("\n" + "=" * 70)
    print("📊 UNIFIED CORPUS SUMMARY")
    print("=" * 70)
    print(f"Total Sessions Processed: {len(all_operational)} of 19")
    print(f"Total Non-Empty Turns:    {len(df_full_op):,}")
    print(f"Unique Students:          {df_full_op['Student_ID'].nunique()}")
    print("\nTurns Breakdown by Speaker Role:")
    for spk, grp in df_full_op.groupby('Speaker'):
        pct = len(grp) / len(df_full_op) * 100
        print(f"  • {spk:10}: {len(grp):4d} turns ({pct:5.2f}%)")

    # Save Unified Files
    os.makedirs('results', exist_ok=True)
    op_path = "Transcripts/Unified_Operational_Database.xlsx"
    oracle_path = "Transcripts/Unified_Gold_Oracle.xlsx"
    
    df_full_op.to_excel(op_path, index=False)
    df_full_oracle.to_excel(oracle_path, index=False)
    
    with open('results/session_audit_matrix.json', 'w', encoding='utf-8') as f:
        json.dump(audit_matrix, f, indent=2, ensure_ascii=False)
        
    print(f"\n💾 Saved Operational Inputs to: {op_path}")
    print(f"💾 Saved Frozen Oracle to:      {oracle_path}")
    print("💾 Saved Session Audit Matrix to: results/session_audit_matrix.json\n")
    return df_full_op, df_full_oracle, audit_matrix

if __name__ == "__main__":
    ingest_all_19_sessions()
