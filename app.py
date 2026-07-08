import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")

# إعداد ملف البيانات
DATA_FILE = "students_data_2027.csv"
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=["م", "الاسم رباعي", "الرقم القومي", "مجموع درجات بالأرقام", "رقم هاتف الواتساب", "(1) الرغبة الأولى:", "(2) الرغبة الثانية:", "(3) الرغبة الثالثة:", "(4) الرغبة الرابعة:", "(5) الرغبة الخامسة والأخيرة:"]).to_csv(DATA_FILE, index=False, encoding='utf-8-sig')

# التصميم
st.markdown('<div style="text-align: center; color: #1E3A8A; font-weight: bold; font-size: 24px;">جامعة المنيا - كلية علوم الرياضة<br>منصة تسجيل رغبات التخصصات (2026-2027)</div>', unsafe_allow_html=True)

# الحقول الأساسية
nat_id = st.text_input("أدخل الرقم القومي (للبحث أو التسجيل الجديد):")
name = st.text_input("الاسم الرباعي:")
score = st.text_input("مجموع الدرجات:")
whatsapp = st.text_input("رقم واتساب:")

# الرغبات
sports = ["كرة القدم", "الكرة الطائرة", "كرة السلة", "كرة اليد", "ألعاب المضرب"]
p1 = st.selectbox("الرغبة الأولى:", ["اختر..."] + sports)
p2 = st.selectbox("الرغبة الثانية:", ["اختر..."] + sports)
p3 = st.selectbox("الرغبة الثالثة:", ["اختر..."] + sports)
p4 = st.selectbox("الرغبة الرابعة:", ["اختر..."] + sports)
p5 = st.selectbox("الرغبة الخامسة:", ["اختر..."] + sports)

# زر الحفظ
if st.button("إرسال واعتماد الرغبات"):
    if not name or not nat_id:
        st.error("يرجى إدخال الاسم والرقم القومي.")
    else:
        df = pd.read_csv(DATA_FILE)
        new_row = pd.DataFrame([{"م": len(df)+1, "الاسم رباعي": name, "الرقم القومي": nat_id, "مجموع درجات بالأرقام": score, "رقم هاتف الواتساب": whatsapp, "(1) الرغبة الأولى:": p1, "(2) الرغبة الثانية:": p2, "(3) الرغبة الثالثة:": p3, "(4) الرغبة الرابعة:": p4, "(5) الرغبة الخامسة والأخيرة:": p5}])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
        st.success("تم الحفظ بنجاح!")

# الإدارة
if st.sidebar.text_input("كلمة المرور:", type="password") == "admin2027":
    with open(DATA_FILE, "rb") as f: st.sidebar.download_button("📥 تحميل البيانات", f, "data.csv")
