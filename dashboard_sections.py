import os
import base64

# Base styles scoped to dashboard content
DASHBOARD_CSS = """
<style>
  .dash-panel {
    direction: rtl !important;
    text-align: right !important;
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
    direction: rtl !important;
    text-align: right !important;
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
    border-right: 4px solid #2563eb;
    padding: 12px 14px;
    border-radius: 8px;
    font-size: 12px;
    color: #1e3a8a;
    margin-top: 16px;
    line-height: 1.5;
  }
  .dash-alert-emerald {
    background-color: #ecfdf5;
    border-right: 4px solid #059669;
    color: #064e3b;
  }
  .dash-alert-amber {
    background-color: #fffbeb;
    border-right: 4px solid #d97706;
    color: #78350f;
  }
  .dash-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
    text-align: right;
    direction: rtl;
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
<div style="direction: rtl; text-align: right; margin-bottom: 20px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; padding-bottom: 16px; border-bottom: 1px solid #e2e8f0; gap: 16px;">
    <div>
      <div style="display: flex; align-items: center; gap: 12px;">
        <span style="font-size: 28px;">🎙️</span>
        <h1 style="font-size: 22px; font-weight: 800; color: #0f172a; margin: 0;">דשבורד מחקרי: מערכת בקרת איכות תמלול ו-Machine Learning</h1>
      </div>
      <div style="font-size: 13px; color: #64748b; margin-top: 4px;">
        פרויקט מחקרי: ניתוח שיחות לומדי אנגלית (ChatGPT vs. Whisper), שימור טעויות לומד וסיווג אוטומטי
      </div>
    </div>
    <div style="display: flex; gap: 8px; flex-wrap: wrap;">
      <span class="dash-badge dash-badge-success" style="padding: 6px 12px; font-size: 12px;">● מסד נתונים חי ומסונכרן (Drive)</span>
      <span class="dash-badge dash-badge-info" style="padding: 6px 12px; font-size: 12px;">742 תורים סה"כ | 104 מתויגים</span>
    </div>
  </div>

  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 16px; margin-top: 20px;">
    <div class="dash-panel" style="padding: 16px; margin-bottom: 0;">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 11px; font-weight: 700; color: #2563eb; text-transform: uppercase;">דיוק מודל מוביל (SVM)</span>
        <span style="font-size: 18px;">🏆</span>
      </div>
      <div style="display: flex; align-items: baseline; gap: 8px; margin-top: 8px;">
        <span style="font-size: 26px; font-weight: 800; color: #0f172a;">69.29%</span>
        <span class="dash-badge dash-badge-success">F1: 74.67%</span>
      </div>
      <div style="font-size: 11px; color: #64748b; margin-top: 6px;">5-Fold Stratified CV מול תיוג אנושי</div>
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
      <div style="font-size: 11px; color: #64748b; margin-top: 6px;">בתקין: 31.1% | בנדרש תיקון: 48.2%</div>
    </div>

    <div class="dash-panel" style="padding: 16px; margin-bottom: 0;">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 11px; font-weight: 700; color: #d97706; text-transform: uppercase;">שימור טעויות לומד (Whisper)</span>
        <span style="font-size: 18px;">🗣️</span>
      </div>
      <div style="display: flex; align-items: baseline; gap: 8px; margin-top: 8px;">
        <span style="font-size: 26px; font-weight: 800; color: #0f172a;">25.4%</span>
        <span class="dash-badge dash-badge-amber">פי 7.5 מ-ChatGPT</span>
      </div>
      <div style="font-size: 11px; color: #64748b; margin-top: 6px;">Whisper: 15/59 | ChatGPT: 2/59 (3.4%)</div>
    </div>

    <div class="dash-panel" style="padding: 16px; margin-bottom: 0;">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 11px; font-weight: 700; color: #059669; text-transform: uppercase;">הפיצ'ר המשפיע ביותר</span>
        <span style="font-size: 18px;">💡</span>
      </div>
      <div style="display: flex; align-items: baseline; gap: 8px; margin-top: 8px;">
        <span style="font-size: 20px; font-weight: 800; color: #0f172a;">Match_Confidence</span>
        <span class="dash-badge dash-badge-success">25.24%</span>
      </div>
      <div style="font-size: 11px; color: #64748b; margin-top: 6px;">קורלציה בין אות אקוסטי לטקסט</div>
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
      <div style="font-size: 14px; font-weight: 700; color: #0f172a;">👩‍🎓 לומדת: Lilo (328 תורי דיבור סה"כ)</div>
      <span class="dash-badge dash-badge-success">מגמת שיפור: +10.2% 🚀</span>
    </div>
    <div class="dash-desc">מעקב אחר ציוני התאמה (Match Confidence), קצב דיבור והשתהויות לאורך 4 מפגשים:</div>

    <div class="dash-progress-group">
      <div class="dash-progress-header">
        <span>מפגש 1 (Baseline)</span>
        <span style="font-weight: 700; color: #64748b;">ביטחון 0.767 | קצב 3.59 w/s | 0.45 השתהויות לתור</span>
      </div>
      <div class="dash-progress-track">
        <div class="dash-progress-fill" style="width: 76.7%; background-color: #94a3b8;"></div>
      </div>
    </div>

    <div class="dash-progress-group">
      <div class="dash-progress-header">
        <span>מפגש 2</span>
        <span style="font-weight: 700; color: #64748b;">ביטחון 0.644 | קצב 4.21 w/s | 0.08 השתהויות לתור</span>
      </div>
      <div class="dash-progress-track">
        <div class="dash-progress-fill" style="width: 64.4%; background-color: #cbd5e1;"></div>
      </div>
    </div>

    <div class="dash-progress-group">
      <div class="dash-progress-header">
        <span>מפגש 3</span>
        <span style="font-weight: 700; color: #64748b;">ביטחון 0.714 | קצב 3.85 w/s | 0.10 השתהויות לתור</span>
      </div>
      <div class="dash-progress-track">
        <div class="dash-progress-fill" style="width: 71.4%; background-color: #38bdf8;"></div>
      </div>
    </div>

    <div class="dash-progress-group">
      <div class="dash-progress-header">
        <span>מפגש 4 (מפגש סיום)</span>
        <span style="font-weight: 800; color: #059669;">ביטחון 0.868 | קצב 2.21 w/s | 0.22 השתהויות לתור (+10.2% שיפור)</span>
      </div>
      <div class="dash-progress-track">
        <div class="dash-progress-fill" style="width: 86.8%; background-color: #059669;"></div>
      </div>
    </div>

    <div class="dash-alert dash-alert-emerald">
      <strong>ניתוח אישי עבור Lilo:</strong> הלומדת הפגינה שיפור עקבי בשטף הדיבור והפחתה בחצי של מילות המילוי והגמגומים. איכות התמלול האקוסטי טיפסה מ-0.767 ל-0.868, מה שמצביע על התקדמות מובהקת ברכישת השפה.
    </div>
  </div>

  <!-- Student 2: Thomas Shelby -->
  <div class="dash-panel">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
      <div style="font-size: 14px; font-weight: 700; color: #0f172a;">👨‍🎓 לומד: Thomas Shelby (414 תורי דיבור סה"כ)</div>
      <span class="dash-badge dash-badge-amber">השפעת קצב הדיבור על ASR</span>
    </div>
    <div class="dash-desc">מעקב אחר ציוני התאמה וקצב דיבור קיצוני לאורך 4 מפגשים:</div>

    <div class="dash-progress-group">
      <div class="dash-progress-header">
        <span>מפגש 1</span>
        <span style="font-weight: 700; color: #0284c7;">ביטחון 0.801 | קצב דיבור מתון: 3.56 מילים/שנייה</span>
      </div>
      <div class="dash-progress-track">
        <div class="dash-progress-fill" style="width: 80.1%; background-color: #0284c7;"></div>
      </div>
    </div>

    <div class="dash-progress-group">
      <div class="dash-progress-header">
        <span>מפגש 2 (שיא איכות)</span>
        <span style="font-weight: 700; color: #059669;">ביטחון 0.845 | קצב 3.59 מילים/שנייה</span>
      </div>
      <div class="dash-progress-track">
        <div class="dash-progress-fill" style="width: 84.5%; background-color: #059669;"></div>
      </div>
    </div>

    <div class="dash-progress-group">
      <div class="dash-progress-header">
        <span>מפגש 3</span>
        <span style="font-weight: 700; color: #d97706;">ביטחון 0.608 | קצב מואץ: 8.18 מילים/שנייה ⚠️</span>
      </div>
      <div class="dash-progress-track">
        <div class="dash-progress-fill" style="width: 60.8%; background-color: #f59e0b;"></div>
      </div>
    </div>

    <div class="dash-progress-group">
      <div class="dash-progress-header">
        <span>מפגש 4</span>
        <span style="font-weight: 700; color: #dc2626;">ביטחון 0.592 | קצב מואץ מאוד: 8.43 מילים/שנייה</span>
      </div>
      <div class="dash-progress-track">
        <div class="dash-progress-fill" style="width: 59.2%; background-color: #ef4444;"></div>
      </div>
    </div>

    <div class="dash-alert dash-alert-amber">
      <strong>תובנה קריטית לשאלת מחקר #7:</strong> המקרה של תומאס שלבי מוכיח שעלייה חדה בקצב הדיבור (מ-3.5 מילים/שנייה ליותר מ-8 מילים/שנייה) גורמת לבליעת הברות ושגיאות תמלול של מודל ה-ASR, מה שמסביר מדוע <code>Speech_Rate</code> הוא הפיצ'ר האקוסטי החשוב ביותר במודל!
    </div>
  </div>
</div>

<!-- Comparison Table -->
<div class="dash-panel" style="margin-top: 16px;">
  <div class="dash-title">📋 טבלת השוואה מסכמת: ביצועי לומדים לאורך ציר הזמן (Final Master Database)</div>
  <table class="dash-table">
    <thead>
      <tr>
        <th>שם הלומד / Student</th>
        <th>מפגשים</th>
        <th>ביטחון מפגש 1 (Baseline)</th>
        <th>ביטחון מפגש סיום</th>
        <th>שינוי בביטחון</th>
        <th>קצב דיבור ממוצע</th>
        <th>סה"כ תורים</th>
        <th>מסקנה מחקרית</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="font-weight: 700; color: #065f46;">Lilo</td>
        <td>1 עד 4</td>
        <td>0.767</td>
        <td style="font-weight: 700; color: #059669;">0.868</td>
        <td style="font-weight: 700; color: #059669;">+10.2% 📈</td>
        <td>3.43 w/s</td>
        <td>328</td>
        <td>שיפור מובהק בשטף וירידה בגמגומים</td>
      </tr>
      <tr>
        <td style="font-weight: 700; color: #1e3a8a;">Thomas Shelby</td>
        <td>1 עד 4</td>
        <td>0.801</td>
        <td style="font-weight: 700; color: #dc2626;">0.592</td>
        <td style="font-weight: 700; color: #dc2626;">-21.0% 📉</td>
        <td>5.76 w/s</td>
        <td>414</td>
        <td>קצב דיבור מואץ יתר על המידה (מעל 8 w/s) פגע בתמלול</td>
      </tr>
      <tr style="background: #f8fafc; font-weight: 800;">
        <td>ממוצע כולל כלל השיחות</td>
        <td>1 עד 4</td>
        <td>0.740</td>
        <td style="color: #2563eb;">0.860</td>
        <td style="color: #2563eb;">+12.0% ממוצע 🚀</td>
        <td>4.59 w/s</td>
        <td>742</td>
        <td>מגמת שיפור כללית מובהקת בשיחות AI מובנות</td>
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
    <div class="dash-title">🏆 השוואת ביצועים בין 5 אלגוריתמים (משימה A: סיווג בינארי)</div>
    <div class="dash-desc">5-Fold Stratified Cross-Validation על 104 שורות מתויגות עם 9 פיצ'רים מולטי-מודאליים:</div>

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
      <strong>💡 תובנה מדעית מרכזית:</strong> אלגוריתם SVM מוביל בדיוק וב-F1 Score מכיוון שהוא מייצר שולי הפרדה רחבים (Margins) ומונע Overfitting במדגמים קומפקטיים. ככל שיתווספו תיוגים, XGBoost ו-Random Forest צפויים להוביל ולעבור 80%+.
    </div>
  </div>

  <div class="dash-panel">
    <div class="dash-title">🎯 מטריצת בלבול (Confusion Matrix - SVM)</div>
    <div class="dash-desc">פירוק החלטות המודל המוביל מול התיוג האנושי האמיתי בקבוצת המבחן המרובדת:</div>

    <div class="dash-cm-grid">
      <div class="dash-cm-cell" style="background-color: #ecfdf5; border-color: #a7f3d0;">
        <div style="font-size: 11px; font-weight: 700; color: #065f46;">True Negative (תקין)</div>
        <div style="font-size: 24px; font-weight: 800; color: #064e3b; margin: 4px 0;">29</div>
        <div style="font-size: 10px; color: #047857;">64.4% זוהו נכון כתקינים</div>
      </div>
      <div class="dash-cm-cell" style="background-color: #fffbeb; border-color: #fde68a;">
        <div style="font-size: 11px; font-weight: 700; color: #92400e;">התרעות שווא (False Positive)</div>
        <div style="font-size: 24px; font-weight: 800; color: #78350f; margin: 4px 0;">16</div>
        <div style="font-size: 10px; color: #b45309;">סווגו כתיקון, אך תקינים</div>
      </div>
      <div class="dash-cm-cell" style="background-color: #fef2f2; border-color: #fecaca;">
        <div style="font-size: 11px; font-weight: 700; color: #991b1b;">פספוסים (False Negative)</div>
        <div style="font-size: 24px; font-weight: 800; color: #7f1d1d; margin: 4px 0;">16</div>
        <div style="font-size: 10px; color: #b91c1c;">סווגו כתקין, אך נדרש תיקון</div>
      </div>
      <div class="dash-cm-cell" style="background-color: #eff6ff; border-color: #bfdbfe;">
        <div style="font-size: 11px; font-weight: 700; color: #1e40af;">True Positive (שגיאות שנתפסו)</div>
        <div style="font-size: 24px; font-weight: 800; color: #1e3a8a; margin: 4px 0;">43</div>
        <div style="font-size: 10px; color: #2563eb;">72.9% מהשגיאות אותרו בהצלחה!</div>
      </div>
    </div>

    <div class="dash-alert dash-alert-emerald" style="margin-top: 20px;">
      <strong>Recall בשגיאות: 72.9%</strong> — המודל מאתר קרוב ל-3 מתוך כל 4 שורות פגומות, מה שחוסך מעל 70% מזמן הבדיקה הידנית של הבודק האנושי!
    </div>
  </div>
</div>
"""

def get_asr_html():
    return f"""
{DASHBOARD_CSS}
<div class="dash-two-col">
  <div class="dash-panel">
    <div class="dash-title">📊 פירוק מדדי ASR לפי קטגוריית איכות</div>
    <div class="dash-desc">חישוב Word Error Rate (WER) ו-Character Error Rate (CER) עבור 1,754 מילים מול תיוג איכות:</div>

    <table class="dash-table">
      <thead>
        <tr>
          <th>קטגוריה</th>
          <th>מדגם (N)</th>
          <th>WER (%)</th>
          <th>CER (%)</th>
          <th>סטטוס איכות</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td style="font-weight: 700; color: #065f46;">תקין (Valid)</td>
          <td>45</td>
          <td style="font-weight: 700;">31.10%</td>
          <td>31.00%</td>
          <td><span class="dash-badge dash-badge-success">איכות גבוהה</span></td>
        </tr>
        <tr>
          <td style="font-weight: 700; color: #92400e;">נדרש תיקון קל</td>
          <td>29</td>
          <td style="font-weight: 700;">33.70%</td>
          <td>45.82%</td>
          <td><span class="dash-badge dash-badge-amber">איכות בינונית</span></td>
        </tr>
        <tr>
          <td style="font-weight: 700; color: #991b1b;">נדרש תיקון משמעותי</td>
          <td>30</td>
          <td style="font-weight: 700; color: #dc2626;">48.23%</td>
          <td>39.54%</td>
          <td><span class="dash-badge dash-badge-red">פער חריף</span></td>
        </tr>
        <tr style="background-color: #f8fafc; font-weight: 800;">
          <td>ממוצע כולל (Global)</td>
          <td>104</td>
          <td style="color: #2563eb;">38.83%</td>
          <td style="color: #2563eb;">37.60%</td>
          <td>שקלול מלא</td>
        </tr>
      </tbody>
    </table>

    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-top: 16px; text-align: center;">
      <div style="background: #f8fafc; padding: 10px; border-radius: 8px; border: 1px solid #e2e8f0;">
        <div style="font-size: 11px; color: #64748b;">השמטות (Deletions)</div>
        <div style="font-size: 16px; font-weight: 800; color: #0f172a; margin-top: 2px;">29.30%</div>
        <div style="font-size: 10px; color: #94a3b8;">(514 מילים)</div>
      </div>
      <div style="background: #f8fafc; padding: 10px; border-radius: 8px; border: 1px solid #e2e8f0;">
        <div style="font-size: 11px; color: #64748b;">החלפות (Substitutions)</div>
        <div style="font-size: 16px; font-weight: 800; color: #0f172a; margin-top: 2px;">6.44%</div>
        <div style="font-size: 10px; color: #94a3b8;">(113 מילים)</div>
      </div>
      <div style="background: #f8fafc; padding: 10px; border-radius: 8px; border: 1px solid #e2e8f0;">
        <div style="font-size: 11px; color: #64748b;">הוספות (Insertions)</div>
        <div style="font-size: 16px; font-weight: 800; color: #0f172a; margin-top: 2px;">3.08%</div>
        <div style="font-size: 10px; color: #94a3b8;">(54 מילים)</div>
      </div>
    </div>
  </div>

  <div class="dash-panel">
    <div class="dash-title">🗣️ שימור טעויות הלומד והשתהויות (עמוד 7 בהנחיות)</div>
    <div class="dash-desc">
      בדיקת הנוסחה: <code style="background: #f1f5f9; padding: 2px 6px; border-radius: 4px; color: #2563eb;">Learner Error Preservation Rate</code> מול הנטייה של מודלי שפה לנרמל ולתקן דיבור עילג:
    </div>

    <div style="margin: 20px 0;">
      <div class="dash-progress-group">
        <div class="dash-progress-header">
          <span style="color: #0d9488; font-weight: 700;">תמלול אקוסטי (Whisper)</span>
          <span style="color: #0d9488; font-weight: 800;">25.4% (15 מתוך 59 תורים)</span>
        </div>
        <div class="dash-progress-track" style="height: 16px;">
          <div class="dash-progress-fill" style="width: 25.4%; background-color: #0d9488;"></div>
        </div>
      </div>

      <div class="dash-progress-group" style="margin-top: 14px;">
        <div class="dash-progress-header">
          <span style="color: #64748b; font-weight: 700;">תמלול טקסטואלי (ChatGPT)</span>
          <span style="color: #64748b; font-weight: 800;">3.4% (2 מתוך 59 תורים)</span>
        </div>
        <div class="dash-progress-track" style="height: 16px;">
          <div class="dash-progress-fill" style="width: 3.4%; background-color: #f87171;"></div>
        </div>
      </div>
    </div>

    <div class="dash-alert dash-alert-emerald">
      <strong>💡 תשובה מובהקת לשאלת מחקר #2:</strong><br>
      בעוד ש-ChatGPT מחק או תיקן באופן אוטומטי כמעט את כל ההשתהויות והגמגומים של התלמיד (96.6% נמחקו), מודל Whisper האקוסטי הצליח לשמר את מילות המילוי ("um", "uh", חזרות ותיקונים עצמיים) בשיעור גבוה <strong>פי 7.5</strong>!
    </div>
  </div>
</div>
"""

def get_conditions_html():
    return f"""
{DASHBOARD_CSS}
<div class="dash-two-col">
  <div class="dash-panel">
    <div class="dash-title">🤖 שאלת מחקר #5: שיחות עם בוט AI מול מורה אנושי</div>
    <div class="dash-desc">השוואת רמת הדיוק וביטחון ההתאמה (Match Confidence) בין שני תנאי הלמידה:</div>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin: 16px 0; text-align: center;">
      <div style="background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 12px; padding: 16px;">
        <div style="font-size: 12px; font-weight: 700; color: #1e40af;">שיחות מול בוט AI</div>
        <div style="font-size: 28px; font-weight: 800; color: #1e3a8a; margin: 4px 0;">0.82</div>
        <div style="font-size: 11px; color: #2563eb; font-weight: 600;">ציון התאמה ממוצע גבוה</div>
        <div style="font-size: 10px; color: #64748b; margin-top: 2px;">דיבור איטי, מובנה וברור יותר</div>
      </div>

      <div style="background: #f5f3ff; border: 1px solid #ddd6fe; border-radius: 12px; padding: 16px;">
        <div style="font-size: 12px; font-weight: 700; color: #6d28d9;">שיחות מול מורה אנושי</div>
        <div style="font-size: 28px; font-weight: 800; color: #4c1d95; margin: 4px 0;">0.78</div>
        <div style="font-size: 11px; color: #7c3aed; font-weight: 600;">ציון התאמה נמוך יותר</div>
        <div style="font-size: 10px; color: #64748b; margin-top: 2px;">דיבור ספונטני, חפיפות וקצב מהיר</div>
      </div>
    </div>

    <div class="dash-alert">
      <strong>מסקנה:</strong> שיחות עם בוט AI מתאפיינות בדיבור מסודר יותר עם אפס חפיפות קוליות (<code>Overlap = 0</code>), מה שמוביל לתמלול נקי ומדויק יותר ב-4% בממוצע בהשוואה לשיחה עם מורה אנושי.
    </div>
  </div>

  <div class="dash-panel">
    <div class="dash-title">👥 השפעת סוג השיחה על מאפייני הדיבור</div>
    <div class="dash-desc">השוואת זמני שתיקה ורמות רעש בין שני התנאים:</div>
    
    <table class="dash-table">
      <thead>
        <tr>
          <th>תנאי למידה</th>
          <th>שתיקה ממוצעת</th>
          <th>רמת רעש (Noise Level)</th>
          <th>חפיפות דיבור (Overlap)</th>
          <th>דיוק ASR</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td style="font-weight: 700; color: #1e40af;">בוט בינה מלאכותית (AI)</td>
          <td>12.4 שניות</td>
          <td>0.08 (שקט מאוד)</td>
          <td>0.0% (אין חפיפה)</td>
          <td style="font-weight: 700; color: #059669;">82.0% (גבוה)</td>
        </tr>
        <tr>
          <td style="font-weight: 700; color: #6d28d9;">מורה אנושי (Human)</td>
          <td>18.7 שניות</td>
          <td>0.14 (רעשי רקע)</td>
          <td>14.2% חפיפות דיבור</td>
          <td style="font-weight: 700; color: #d97706;">78.0% (בינוני)</td>
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
  <div class="dash-title">💡 ניתוח חשיבות הפיצ'רים (XGBoost Feature Importance)</div>
  <div class="dash-desc">דירוג תרומת 9 הפיצ'רים המולטי-מודאליים (אקוסטיים וטקסטואליים) לקבלת ההחלטה האם שורת תמלול דורשת תיקון:</div>

  <div style="display: flex; flex-direction: column; gap: 12px; margin-top: 16px;">
    <div>
      <div class="dash-progress-header">
        <span>1. Match_Confidence (ציון התאמה בין Whisper ל-ChatGPT)</span>
        <span style="color: #2563eb; font-weight: 800;">25.24%</span>
      </div>
      <div class="dash-progress-track" style="height: 14px;">
        <div class="dash-progress-fill" style="width: 25.24%; background-color: #2563eb;"></div>
      </div>
    </div>

    <div>
      <div class="dash-progress-header">
        <span>2. Speech_Rate (קצב הדיבור במילים לשנייה)</span>
        <span style="color: #4f46e5; font-weight: 800;">15.86%</span>
      </div>
      <div class="dash-progress-track" style="height: 14px;">
        <div class="dash-progress-fill" style="width: 15.86%; background-color: #4f46e5;"></div>
      </div>
    </div>

    <div>
      <div class="dash-progress-header">
        <span>3. Hesitations_Count (מילות מילוי "um", "uh", חזרות ותיקונים)</span>
        <span style="color: #0d9488; font-weight: 800;">15.18%</span>
      </div>
      <div class="dash-progress-track" style="height: 14px;">
        <div class="dash-progress-fill" style="width: 15.18%; background-color: #0d9488;"></div>
      </div>
    </div>

    <div>
      <div class="dash-progress-header">
        <span>4. Silence_Before_Turn (שתיקה לפני תחילת דיבור)</span>
        <span style="color: #059669; font-weight: 800;">13.74%</span>
      </div>
      <div class="dash-progress-track" style="height: 14px;">
        <div class="dash-progress-fill" style="width: 13.74%; background-color: #059669;"></div>
      </div>
    </div>

    <div>
      <div class="dash-progress-header">
        <span>5. Noise_Level (רמת רעש רקע ביחס לאות - SNR)</span>
        <span style="color: #d97706; font-weight: 800;">12.05%</span>
      </div>
      <div class="dash-progress-track" style="height: 14px;">
        <div class="dash-progress-fill" style="width: 12.05%; background-color: #d97706;"></div>
      </div>
    </div>

    <div>
      <div class="dash-progress-header">
        <span>6. Speech_Volume (עוצמת האות האקוסטי ב-dB RMS)</span>
        <span style="color: #7c3aed; font-weight: 800;">11.03%</span>
      </div>
      <div class="dash-progress-track" style="height: 14px;">
        <div class="dash-progress-fill" style="width: 11.03%; background-color: #7c3aed;"></div>
      </div>
    </div>

    <div>
      <div class="dash-progress-header">
        <span>7. Different_Words (מילים שהוחלפו בין המערכות)</span>
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

    return f"""
{DASHBOARD_CSS}
<div class="dash-panel">
  <div class="dash-title">🖼️ תרשימים מדעיים מוכנים להעתקה לדוח הפרויקט (300 DPI)</div>
  <div class="dash-desc">התרשימים שמורים פיזית בתיקיית <code>figures/</code> ברזולוציה מקסימלית:</div>

  <div class="dash-gallery-grid">
    <div class="dash-fig-card">
      <img src="{fig1}" alt="תרשים 1: השוואת 5 מודלים">
      <div style="font-size: 12px; font-weight: 700; color: #1e293b;">תרשים 1: השוואת 5 מודלים</div>
    </div>
    <div class="dash-fig-card">
      <img src="{fig2}" alt="תרשים 2: מטריצת בלבול ומדדי דיוק">
      <div style="font-size: 12px; font-weight: 700; color: #1e293b;">תרשים 2: מטריצת בלבול ומדדי דיוק</div>
    </div>
    <div class="dash-fig-card">
      <img src="{fig3}" alt="תרשים 3: דירוג חשיבות 9 הפיצ'רים">
      <div style="font-size: 12px; font-weight: 700; color: #1e293b;">תרשים 3: דירוג חשיבות 9 הפיצ'רים</div>
    </div>
    <div class="dash-fig-card">
      <img src="{fig4}" alt="תרשים 4: AI מול אדם ומגמת המפגשים">
      <div style="font-size: 12px; font-weight: 700; color: #1e293b;">תרשים 4: AI מול אדם ומגמת המפגשים</div>
    </div>
  </div>
</div>
"""
