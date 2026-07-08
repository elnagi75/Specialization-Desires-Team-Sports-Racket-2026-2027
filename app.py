import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="منصة تسجيل الرغبات", layout="wide", initial_sidebar_state="collapsed")

DATA_FILE = "students_data_2027.csv"
COLUMNS = ["م", "الاسم رباعي", "الرقم القومي", "مجموع درجات بالأرقام", "رقم هاتف الواتساب", "(1) الرغبة الأولى:", "(2) الرغبة الثانية:", "(3) الرغبة الثالثة:", "(4) الرغبة الرابعة:", "(5) الرغبة الخامسة والأخيرة:"]

if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=COLUMNS).to_csv(DATA_FILE, index=False, encoding='utf-8-sig')

st.markdown("""
    <style>
    div[data-testid="stMarkdownContainer"] p, h1, h2, h3, h4, h5, h6, label { text-align: right !important; direction: rtl !important; }
    .instructions-box { background-color: #F8FAFC; border-right: 8px solid #1E3A8A; padding: 30px; margin-bottom: 25px; direction: rtl; text-align: right; }
    .instructions-box h4 { color: #DC2626; font-weight: 900 !important; font-size: 26px !important; }
    .instructions-box ol { font-weight: bold !important; font-size: 20px !important; line-height: 2 !important; color: #111827; }
    div.stButton > button { background-color: #1E3A8A; color: white; font-weight: bold; font-size: 22px; width: 100%; padding: 15px; }
    </style>
""", unsafe_allow_html=True)

# لوحة الإدارة
st.sidebar.markdown("### لوحة تحكم الإدارة")
if st.sidebar.text_input("كلمة المرور:", type="password") == "admin2027":
    with open(DATA_FILE, "rb") as f: st.sidebar.download_button("📥 تحميل البيانات (Excel)", f, "students_data_2027.csv")

# الترويسة
st.markdown('<div style="text-align: center; font-weight: bold; color: #1E3A8A; font-size: 24px;">جامعة المنيا - كلية علوم الرياضة<br>منصة تسجيل رغبات التخصصات (2026-2027)</div>', unsafe_allow_html=True)

# البحث
df = pd.read_csv(DATA_FILE).astype(str)
national_id = st.text_input("أدخل الرقم القومي (14 رقماً) لعرض بياناتك أو التسجيل:", max_chars=14)
student = df[df["الرقم القومي"] == national_id] if national_id and national_id in df["الرقم القومي"].values else pd.DataFrame()

# التعليمات
st.markdown("""<div class="instructions-box"><h4>تعليمات تسجيل الرغبات:</h4><ol>
<li>تأكد جيداً من ترتيب رغباتك قبل بدء التسجيل بما يحقق طموحك الأكاديمي.</li>
<li>يمكنك تعديل رغباتك بعد الحفظ باستخدام رقمك القومي طوال فترة التسجيل من يوم ( / / 2026 ) حتى يوم ( / / 2026 ).</li>
<li>بعد غلق المنصة، تُعتمد آخر رغبات مسجلة نهائياً، ولا يُسمح بأي تعديل.</li>
<li>اكتب الرقم القومي كاملاً بدقة: 14 رقماً، فهو وسيلة الدخول للتسجيل أو التعديل.</li>
<li>اكتب مجموع الدرجات بالأرقام فقط كما هو معلن، دون نسبة مئوية.</li>
<li>رتب الرغبات الخمس بعناية، النظام يمنع تكرار التخصص.</li>
<li>أدخل رقم واتساب صحيحاً (11 رقماً).</li></ol></div>""", unsafe_allow_html=True)

# الحقول
name = st.text_input("الاسم الرباعي:", value=student.iloc[0]["الاسم رباعي"] if not student.empty else "")
score = st.text_input("مجموع الدرجات:", value=student.iloc[0]["مجموع درجات بالأرقام"] if not student.empty else "")
whatsapp = st.text_input("رقم واتساب:", value=student.iloc[0]["رقم هاتف الواتساب"] if not student.empty else "", max_chars=11)

# الرغبات
sports = ["كرة القدم", "الكرة الطائرة", "كرة السلة", "كرة اليد", "ألعاب المضرب"]
def get_idx(val, opts): return opts.index(val) + 1 if val in opts else 0
p1 = st.selectbox("الرغبة الأولى:", ["اختر التخصص..."] + sports, index=get_idx(student.iloc[0]["(1) الرغبة الأولى:"] if not student.empty else "", sports))
p2 = st.selectbox("الرغبة الثانية:", ["اختر التخصص..."] + [s for s in sports if s != p1], index=get_idx(student.iloc[0]["(2) الرغبة الثانية:"] if not student.empty else "", [s for s in sports if s != p1]))
p3 = st.selectbox("الرغبة الثالثة:", ["اختر التخصص..."] + [s for s in sports if s not in [p1, p2]], index=get_idx(student.iloc[0]["(3) الرغبة الثالثة:"] if not student.empty else "", [s for s in sports if s not in [p1, p2]]))
p4 = st.selectbox("الرغبة الرابعة:", ["اختر التخصص..."] + [s for s in sports if s not in [p1, p2, p3]], index=get_idx(student.iloc[0]["(4) الرغبة الرابعة:"] if not student.empty else "", [s for s in sports if s not in [p1, p2, p3]]))
p5 = st.selectbox("الرغبة الخامسة:", ["اختر التخصص..."] + [s for s in sports if s not in [p1, p2, p3, p4]], index=get_idx(student.iloc[0]["(5) الرغبة الخامسة والأخيرة:"] if not student.empty else "", [s for s in sports if s not in [p1, p2, p3, p4]]))

if st.button("إرسال واعتماد الرغبات"):
    if not name or not national_id or not score or not whatsapp or "اختر" in [p1,p2,p3,p4,p5]: st.error("يرجى استكمال البيانات.")
    else:
        if not student.empty:
            df.loc[df["الرقم القومي"] == national_id, ["الاسم رباعي", "مجموع درجات بالأرقام", "رقم هاتف الواتساب", "(1) الرغبة الأولى:", "(2) الرغبة الثانية:", "(3) الرغبة الثالثة:", "(4) الرغبة الرابعة:", "(5) الرغبة الخامسة والأخيرة:"]] = [name, score, whatsapp, p1, p2, p3, p4, p5]
            st.success("تم التحديث بنجاح!")
        else:
            new_row = pd.DataFrame([{"م": len(df)+1, "الاسم رباعي": name, "الرقم القومي": national_id, "مجموع درجات بالأرقام": score, "رقم هاتف الواتساب": whatsapp, "(1) الرغبة الأولى:": p1, "(2) الرغبة الثانية:": p2, "(3) الرغبة الثالثة:": p3, "(4) الرغبة الرابعة:": p4, "(5) الرغبة الخامسة والأخيرة:": p5}])
            df = pd.concat([df, new_row], ignore_index=True)
            st.success("تم التسجيل بنجاح!")
        df.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
