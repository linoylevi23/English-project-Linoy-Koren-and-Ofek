#!/usr/bin/env python3
"""
Grammar Corrector & Sentence Normalizer
=======================================
Generates grammatically corrected English target sentences for speech turns,
cleans conversational disfluencies/stutters, classifies ESL error categories,
and updates the 'Corrected Sentence' column in Final_Master_Database.xlsx.
"""

import os
import re
import pandas as pd
import numpy as np

MASTER_PATH = "Transcripts/Final_Master_Database.xlsx"

# Common ESL collocation and grammar replacements
SPECIFIC_CORRECTIONS = {
    # Collocations & Idioms
    r"\bmake a trip\b": "take a trip",
    r"\bmake trips\b": "take trips",
    r"\bto make a trip\b": "to take a trip",
    r"\bmaking a trip\b": "taking a trip",
    r"\beat something outside\b": "eat out",
    r"\beating something outside\b": "eating out",
    r"\bspinoff for\b": "spin-off of",
    r"\bspin off for\b": "spin-off of",
    r"\bto this week\b": "this week",
    r"\bin all over the\b": "all over the",
    r"\bnext week exam\b": "exam next week",
    r"\bwith device\b": "with devices",
    r"\bwith the device\b": "with devices",
    r"\bhands-on experience\. With device\b": "hands-on experience with devices",
    
    # Common ESL Verb Tense & Agreement Errors
    r"\bnothing interesting happen today\b": "nothing interesting happened today",
    r"\bnothing interesting happen\b": "nothing interesting happened",
    r"\bit\u05f3s was wonderful\b": "it was wonderful",
    r"\bit's was wonderful\b": "it was wonderful",
    r"\bit\u05f3s was\b": "it was",
    r"\bit's was\b": "it was",
    r"\blast time we hang out\b": "last time we hung out",
    r"\bwe go to the sea\b": "we went to the beach",
    r"\bwe go to the beach\b": "we went to the beach",
    r"\byou can say it again\?\b": "could you say that again?",
    r"\bcan you say it again\?\b": "could you say that again?",
    r"\bcan you say it more slowly\?\b": "could you say that more slowly?",
    r"\bwhat\? you can say it again\?\b": "could you please say that again?",
    r"\bwhat\? say it again\b": "pardon? Could you say that again?",
    r"\bwhat say it again\b": "could you say that again?",
    r"\banother time\?\b": "could you repeat that one more time?",
    
    # Common Casing & Contractions
    r"\bIve\b": "I've",
    r"\bive\b": "I've",
    r"\bits basically\b": "it's basically",
    r"\bits a\b": "it's a",
    r"\bits one\b": "it's one",
    r"\bits my\b": "it's my",
    r"\bcant\b": "can't",
    r"\bdont\b": "don't",
    r"\bwont\b": "won't",
    r"\bdidnt\b": "didn't",
    r"\bdoesnt\b": "doesn't",
    r"\bwasnt\b": "wasn't",
    r"\bhouse of the dragon\b": "House of the Dragon",
    r"\bgame of thrones\b": "Game of Thrones",
    r"\bfunko pops\b": "Funko Pops",
    r"\bfunko pop\b": "Funko Pop",
    r"\bidf\b": "IDF",
}

DISFLUENCY_PATTERNS = [
    r"\b(ah|uh|um|er|hmm|mmm|mhm)\b[\.,]?",
    r"\b([A-Za-z]+)\.\.\s+\1\b",          # e.g. "Can you.. Can you"
    r"\b([A-Za-z]+)\s+\1\b",               # e.g. "walking walking", "early early"
    r"\bin my\s+in my\b",                  # specific stutter
    r"\bin my free time,\s+in my free time\b",
    r"\bthe\.\.\s+the\b",
    r"\bthe\.\.\s+what\b",
    r"\bto the\.\.\s+the\b"
]


def classify_error(orig: str, corrected: str) -> str:
    """Classifies the primary linguistic error between original and corrected sentences."""
    if orig.strip() == corrected.strip():
        return "Valid / Standard"
    
    orig_l = orig.lower()
    corr_l = corrected.lower()

    if any(k in orig_l for k in ["make a trip", "eat something outside", "spinoff for", "device", "training, also"]):
        return "Collocation & Word Choice"
    
    if any(k in orig_l for k in ["happen today", "we hang out", "we go", "it's was", "it\u05f3s was"]):
        return "Verb Tense & Agreement"
        
    if any(k in orig_l for k in ["to this week", "in all over", "say it more slowly", "you can say it"]):
        return "Preposition & Syntax"
        
    if any(re.search(pat, orig_l) for pat in DISFLUENCY_PATTERNS):
        return "Speech Disfluency & Stutter"
        
    if any(k in orig_l for k in ["ive", "its a", "cant", "dont", "funko", "dragon", "thrones"]):
        return "Punctuation & Mechanics"

    return "Grammar & Phrasing"


def correct_sentence(text: str) -> str:
    """Applies ESL grammar corrections, disfluency cleaning, and standard punctuation."""
    if pd.isna(text) or not str(text).strip() or str(text).strip().lower() == "nan":
        return ""
        
    res = str(text).strip()
    
    # 1. Apply specific ESL fixes
    for pat, repl in SPECIFIC_CORRECTIONS.items():
        res = re.sub(pat, repl, res, flags=re.IGNORECASE)
        
    # 2. Clean stutters / disfluencies
    # Repeated single words: "walking, walking" -> "walking", "early, early" -> "early"
    res = re.sub(r'\b([A-Za-z]+)[,\s]+\1\b', r'\1', res, flags=re.IGNORECASE)
    res = re.sub(r'\b([A-Za-z]+)\.\.\s+\1\b', r'\1', res, flags=re.IGNORECASE)
    res = re.sub(r'\b(in my free time)[,\s]+\1\b', r'\1', res, flags=re.IGNORECASE)
    res = re.sub(r'\b(Ah\s+wow|Ah,\s+wow|Wow)[,\s]+', '', res, flags=re.IGNORECASE)
    res = re.sub(r'\b(uh|um|er|hmm|mmm)\b[,\s]*', '', res, flags=re.IGNORECASE)
    res = re.sub(r'\.\.\s*', ' ', res)
    res = re.sub(r'\s{2,}', ' ', res)

    # 3. Clean trailing / dangling punctuation
    res = res.strip(' ,;')
    if res and res[-1] not in '.!?':
        res += '.'
        
    # 4. Capitalize first letter of sentences
    sentences = re.split(r'([.!?]\s+)', res)
    cap_sentences = []
    for s in sentences:
        if s and s[0].isalpha():
            cap_sentences.append(s[0].upper() + s[1:])
        else:
            cap_sentences.append(s)
    res = ''.join(cap_sentences)
    
    # 5. Handle pronoun 'I' casing
    res = re.sub(r'\bi\b', 'I', res)
    res = re.sub(r'\bi\'', "I'", res)
    
    return res.strip()


def run_pipeline():
    print(f"📖 Loading database from: {MASTER_PATH}")
    df = pd.read_excel(MASTER_PATH)
    total = len(df)
    print(f"   Found {total} records.")
    
    if "Corrected Sentence" not in df.columns:
        df["Corrected Sentence"] = pd.Series(index=df.index, dtype="object")
    else:
        df["Corrected Sentence"] = df["Corrected Sentence"].astype("object")

    if "Grammar_Error_Type" not in df.columns:
        df["Grammar_Error_Type"] = pd.Series(index=df.index, dtype="object")

    corrected_count = 0
    error_type_counts = {}

    for idx, row in df.iterrows():
        # Prefer ChatGPT transcript if clean, fallback to Additional ASR
        chat_t = str(row.get("ChatGPT Transcript", "")).strip()
        whisp_t = str(row.get("Additional ASR Transcript", "")).strip()
        
        orig = chat_t if (chat_t and chat_t != "nan") else whisp_t
        if not orig or orig == "nan":
            orig = ""
            
        corrected = correct_sentence(orig)
        err_type = classify_error(orig, corrected)
        
        df.at[idx, "Corrected Sentence"] = corrected
        df.at[idx, "Grammar_Error_Type"] = err_type
        
        if orig.strip() != corrected.strip():
            corrected_count += 1
        error_type_counts[err_type] = error_type_counts.get(err_type, 0) + 1

    # Save to Excel
    df.to_excel(MASTER_PATH, index=False)
    print(f"\n✅ Successfully updated 'Corrected Sentence' across {total} records!")
    print(f"   • Turns requiring grammatical/stylistic modification: {corrected_count} ({corrected_count/total*100:.1f}%)")
    print(f"   • Error category distribution:")
    for err, cnt in sorted(error_type_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"     - {err}: {cnt} turns ({cnt/total*100:.1f}%)")

if __name__ == "__main__":
    run_pipeline()
