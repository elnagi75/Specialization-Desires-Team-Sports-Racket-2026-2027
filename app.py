import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="منصة تسجيل الرغبات", layout="wide", initial_sidebar_state="collapsed")
DATA_FILE = "students_data_2027.csv"
if not os.path.exists(DATA_FILE): pd.DataFrame(columns=["م", "الاسم رباعي", "الرقم القومي", "مجموع درجات بالأرقام", "رقم هاتف الواتساب", "(1) الرغبة الأولى:", "(2) الرغبة الثانية:", "(3) الرغبة الثالثة:", "(4) الرغبة الرابعة:", "(5) الرغبة الخامسة والأخيرة:"]).to_csv(DATA_FILE, index=False, encoding='utf-8-sig')

st.markdown("""<style>.instructions-box { background-color: #F8FAFC; border-right: 8px solid #1E3A8A; padding: 20px; margin-bottom: 25px; text-align: right; }
h4 { color: #DC2626; } ol { font-weight: bold; font-size: 18px; }</style>""", unsafe_allow_html=True)

# لوحة الإدارة
if st.sidebar.text_input("كلمة المرور:", type="password") == "admin2027":
    with open(DATA_FILE, "rb") as f: st.sidebar.download_button("📥 تحميل البيانات", f, "data.csv")

st.markdown('<div style="text-align: center; font-weight: bold; color: #1E3A8A; font-size: 24px;">جامعة المنيا - كلية علوم الرياضة<br>منصة تسجيل الرغبات (2026-2027)</div>', unsafe_allow_html=True)

# التعليمات
st.markdown("""<div class="instructions-box"><h4>تعليمات تسجيل الرغبات:</h4><ol>
<li>تأكد جيداً من ترتيب رغباتك قبل بدء التسجيل.</li>
<li>يمكنك تعديل رغباتك باستخدام رقمك القومي طوال فترة التسجيل.</li>
<li>بعد غلق المنصة، تُعتمد آخر رغبات مسجلة نهائياً.</li>
<li>اكتب الرقم القومي كاملاً (14 رقماً)، فهو وسيلة الدخول للتسجيل أو التعديل.</li>
<li>اكتب مجموع الدرجات بالأرقام فقط، دون رموز.</li>
<li>النظام يمنع تكرار التخصص.</li>
<li>أدخل رقم واتساب صحيح (11 رقماً).</li></ol></div>""", unsafe_allow_html=True)

# استرجاع البيانات
df = pd.read_csv(DATA_FILE).astype(str)
nat_id = st.text_input("أدخل الرقم القومي لعرض بياناتك أو التسجيل:")
student = df[df["الرقم القومي"] == nat_id] if nat_id in df["الرقم القومي"].values else pd.DataFrame()

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
    if not name or not nat_id or not score or not whatsapp or "اختر" in [p1,p2,p3,p4,p5]: st.error("يرجى استكمال كافة البيانات.")
    else:
        if not student.empty:
            df.loc[df["الرقم القومي"] == nat_id, ["الاسم رباعي", "مجموع درجات بالأرقام", "رقم هاتف الواتساب", "(1) الرغبة الأولى:", "(2) الرغبة الثانية:", "(3) الرغبة الثالثة:", "(4) الرغبة الرابعة:", "(5) الرغبة الخامسة والأخيرة:"]] = [name, score, whatsapp, p1, p2, p3, p4, p5]
            st.success("تم التحديث بنجاح!")
        else:
            new_row = pd.DataFrame([{"م": len(df)+1, "الاسم رباعي": name, "الرقم القومي": nat_id, "مجموع درجات بالأرقام": score, "رقم هاتف الواتساب": whatsapp, "(1) الرغبة الأولى:": p1, "(2) الرغبة الثانية:": p2, "(3) الرغبة الثالثة:": p3, "(4) الرغبة الرابعة:": p4, "(5) الرغبة الخامسة والأخيرة:": p5}])
            df = pd.concat([df, new_row], ignore_index=True)
            st.success("تم التسجيل بنجاح!")
        df.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
