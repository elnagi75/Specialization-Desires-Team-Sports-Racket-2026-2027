import streamlit as st
import pandas as pd
import os

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة تسجيل الرغبات - جامعة المنيا", layout="wide", initial_sidebar_state="collapsed")

# 2. ملف البيانات
DATA_FILE = "students_data_2027.csv"

COLUMNS = [
    "م", 
    "الاسم رباعي", 
    "الرقم القومي", 
    "مجموع درجات بالأرقام (بدون نسب مئؤية)", 
    "رقم هاتف الواتساب", 
    "(1) الرغبة الأولى:", 
    "(2) الرغبة الثانية:", 
    "(3) الرغبة الثالثة:", 
    "(4) الرغبة الرابعة:", 
    "(5) الرغبة الخامسة والأخيرة:"
]

if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=COLUMNS)
    df_init.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')

# 3. التصميم البصري الأنيق (CSS)
st.markdown("""
    <style>
    div[data-testid="stMarkdownContainer"] p, h1, h2, h3, h4, h5, h6, label {
        text-align: right !important;
        direction: rtl !important;
    }
    .header-text { text-align: center !important; font-weight: bold; color: #1E3A8A; font-size: 24px; line-height: 1.6; direction: rtl; }
    .instructions-box { background-color: #F8FAFC; border-right: 8px solid #1E3A8A; padding: 30px; border-radius: 8px; margin-top: 20px; margin-bottom: 25px; direction: rtl; text-align: right; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .instructions-box h4 { color: #DC2626; margin-top: 0; font-weight: 900 !important; font-size: 26px !important; border-bottom: 2px solid #CBD5E1; padding-bottom: 10px; }
    .instructions-box ol { font-weight: bold !important; font-size: 20px !important; line-height: 2 !important; color: #111827; margin-right: 20px; }
    .instructions-box li { margin-bottom: 12px; }
    .logo-placeholder { border: 2px dashed #CBD5E1; padding: 20px; text-align: center; border-radius: 8px; color: #64748B; font-size: 14px; margin-top: 15px; }
    div.stButton > button:first-child { background-color: #1E3A8A; color: white; font-weight: bold; font-size: 22px; padding: 15px; margin-top: 20px; border-radius: 8px;}
    .stSelectbox label, .stTextInput label { font-size: 20px !important; font-weight: bold !important; color: #1E3A8A; }
    </style>
""", unsafe_allow_html=True)

# 4. لوحة تحكم الإدارة
st.sidebar.markdown("<h3 style='text-align: right; direction: rtl;'>لوحة تحكم الإدارة</h3>", unsafe_allow_html=True)
if st.sidebar.text_input("أدخل كلمة المرور:", type="password") == "admin2027":
    st.sidebar.success("✅ تم تسجيل الدخول للإدارة")
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as file:
            st.sidebar.download_button("📥 تحميل بيانات الطلاب (Excel)", file, "البيانات_النهائية_لتنسيق_الطلاب_2027.csv", "text/csv")

# 5. الترويسة والشعارات
col1, col2, col3 = st.columns([1, 3, 1])
with col1: 
    if os.path.exists("fac_logo.png"): st.image("fac_logo.png", use_container_width=True)
    else: st.markdown('<div class="logo-placeholder">مصر<br>[ مكان شعار كلية علوم الرياضة ]</div>', unsafe_allow_html=True)
with col2:
    st.markdown('''
        <div class="header-text">جامعة المنيا - كلية علوم الرياضة<br>قسم الرياضات الجماعية وألعاب المضرب<br>
        <span style="color: #2563EB; font-size: 22px;">منصة تسجيل رغبات التخصصات لطلاب الفرقة الرابعة للعام الجامعي 2027/2026</span></div>
    ''', unsafe_allow_html=True)
with col3: 
    if os.path.exists("uni_logo.png"): st.image("uni_logo.png", use_container_width=True)
    else: st.markdown('<div class="logo-placeholder">جامعة المنيا<br>[ مكان شعار جامعة المنيا ]</div>', unsafe_allow_html=True)

st.markdown("<br><hr>", unsafe_allow_html=True)

# 6. صندوق التعليمات
st.markdown("""
<div class="instructions-box">
    <h4>تعليمات تسجيل الرغبات:</h4>
    <ol>
        <li>تأكد جيداً من ترتيب رغباتك قبل بدء التسجيل بما يحقق طموحك الأكاديمي.</li>
        <li>يمكنك تعديل رغباتك بعد الحفظ أكثر من مرة باستخدام رقمك القومي طوال فترة التسجيل من يوم ( / / 2026 ) حتى يوم ( / / 2026 ).</li>
        <li>بعد غلق المنصة، تُعتمد آخر رغبات مسجلة نهائياً، ولا يُسمح بأي تعديل أو تغيير تخصص.</li>
        <li>اكتب الرقم القومي كاملاً بدقة: 14 رقماً باللغة الإنجليزية، فهو وسيلة الدخول للتسجيل أو التعديل.</li>
        <li>اكتب مجموع الدرجات بالأرقام فقط كما هو معلن بالكشوف الرسمية، دون نسبة مئوية أو أي رموز.</li>
        <li>رتب الرغبات الخمس بعناية، مع العلم أن النظام يمنع تكرار التخصص.</li>
        <li>أدخل رقم واتساب صحيحاً ومفعلاً مكوناً من 11 رقماً للتواصل الرسمي عند الحاجة.</li>
    </ol>
</div>
""", unsafe_allow_html=True)

# 7. قراءة البيانات بأمان
df = pd.read_csv(DATA_FILE).astype(str)

# 8. القسم الأول: البيانات الأساسية
st.markdown('<h3 style="color: #1E3A8A; font-weight: bold; font-size: 24px;">أولاً: البيانات الأساسية</h3>', unsafe_allow_html=True)

national_id = st.text_input("الرقم القومي (14 رقماً) - أدخله أولاً لعرض بياناتك للتعديل أو للتسجيل الجديد:", max_chars=14)

# استرجاع البيانات الأساسية فقط إن وجدت
student_data = df[df["الرقم القومي"] == str(national_id)] if national_id and len(national_id) == 14 else pd.DataFrame()

def_name = student_data.iloc[0]["الاسم رباعي"] if not student_data.empty else ""
def_score = student_data.iloc[0]["مجموع درجات بالأرقام (بدون نسب مئؤية)"] if not student_data.empty else ""
def_phone = student_data.iloc[0]["رقم هاتف الواتساب"] if not student_data.empty else ""

col_left, col_right = st.columns(2)
with col_right:
    name = st.text_input("الاسم الرباعي:", value=def_name)
with col_left:
    score = st.text_input("مجموع الدرجات بالأرقام (بدون أي علامات):", value=def_score)
    whatsapp = st.text_input("رقم هاتف الواتساب (11 رقماً):", value=def_phone, max_chars=11)

st.markdown("<hr>", unsafe_allow_html=True)

# 9. القسم الثاني: الرغبات
st.markdown('<h3 style="color: #1E3A8A; font-weight: bold; font-size: 24px;">ثانياً: ترتيب الرغبات التخصصية</h3>', unsafe_allow_html=True)

spacer_right, center_col, spacer_left = st.columns([1, 2, 1])

with center_col:
    st.info("💡 قم باختيار الرغبة الأولى لتفعيل باقي الرغبات. لا يمكن اختيار نفس التخصص مرتين.")
    all_sports = ["كرة القدم", "الكرة الطائرة", "كرة السلة", "كرة اليد", "ألعاب المضرب"]

    # تم إلغاء تذكر الرغبات.. تبدأ فارغة دائماً لتجنب إرباك الطالب
    pref1 = st.selectbox("الرغبة الأولى:", ["اختر التخصص..."] + all_sports)

    options2 = ["اختر التخصص..."] + [s for s in all_sports if s != pref1]
    pref2 = st.selectbox("الرغبة الثانية:", options2, disabled=(pref1 == "اختر التخصص..."))

    options3 = ["اختر التخصص..."] + [s for s in all_sports if s not in [pref1, pref2]]
    pref3 = st.selectbox("الرغبة الثالثة:", options3, disabled=(pref2 == "اختر التخصص..."))

    options4 = ["اختر التخصص..."] + [s for s in all_sports if s not in [pref1, pref2, pref3]]
    pref4 = st.selectbox("الرغبة الرابعة:", options4, disabled=(pref3 == "اختر التخصص..."))

    options5 = ["اختر التخصص..."] + [s for s in all_sports if s not in [pref1, pref2, pref3, pref4]]
    pref5 = st.selectbox("الرغبة الخامسة والأخيرة:", options5, disabled=(pref4 == "اختر التخصص..."))

st.markdown("<br>", unsafe_allow_html=True)

# 10. الاعتماد والحفظ
if st.button("إرسال واعتماد الرغبات نهائياً", use_container_width=True):
    if not name or not national_id or not score or not whatsapp or pref1 == "اختر التخصص..." or pref5 == "اختر التخصص...":
        st.error("❌ يرجى استكمال جميع البيانات وتحديد الرغبات الخمس قبل الإرسال.")
    elif len(national_id) != 14 or not national_id.isdigit():
        st.error("❌ عذراً.. الرقم القومي يجب أن يتكون من 14 رقماً صحيحاً.")
    elif len(whatsapp) != 11 or not whatsapp.isdigit():
        st.error("❌ عذراً.. رقم الواتساب يجب أن يتكون من 11 رقماً صحيحاً.")
    else:
        df = pd.read_csv(DATA_FILE).astype(str)
        
        if str(national_id) in df["الرقم القومي"].values:
            idx = df.index[df['الرقم القومي'] == str(national_id)].tolist()[0]
            df.loc[idx, "الاسم رباعي"] = name
            df.loc[idx, "مجموع درجات بالأرقام (بدون نسب مئؤية)"] = str(score)
            df.loc[idx, "رقم هاتف الواتساب"] = str(whatsapp)
            df.loc[idx, "(1) الرغبة الأولى:"] = pref1
            df.loc[idx, "(2) الرغبة الثانية:"] = pref2
            df.loc[idx, "(3) الرغبة الثالثة:"] = pref3
            df.loc[idx, "(4) الرغبة الرابعة:"] = pref4
            df.loc[idx, "(5) الرغبة الخامسة والأخيرة:"] = pref5
            
            df.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
            st.success(f"🔄 تم تحديث رغباتك بنجاح يا {name}. تم اعتماد التعديل الأخير.")
        else:
            new_row = pd.DataFrame([{
                "م": str(len(df) + 1),
                "الاسم رباعي": name,
                "الرقم القومي": str(national_id),
                "مجموع درجات بالأرقام (بدون نسب مئؤية)": str(score),
                "رقم هاتف الواتساب": str(whatsapp),
                "(1) الرغبة الأولى:": pref1,
                "(2) الرغبة الثانية:": pref2,
                "(3) الرغبة الثالثة:": pref3,
                "(4) الرغبة الرابعة:": pref4,
                "(5) الرغبة الخامسة والأخيرة:": pref5
            }])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
            st.success(f"✅ تم حفظ رغباتك بنجاح واعتمادها يا {name}. نتمنى لك التوفيق!")
