import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="تسجيل الرغبات - الرياضات الجماعية", layout="centered", page_icon="📝")

# توجيه النص من اليمين لليسار
st.markdown("""
    <style>
    body { direction: RTL; text-align: right; }
    p, h1, h2, h3, h4, h5, h6, .stSelectbox label, .stTextInput label { text-align: right; }
    </style>
""", unsafe_allow_html=True)

st.title("منصة تسجيل الرغبات - الرياضات الجماعية وألعاب المضرب (2026-2027)")
st.write("مرحباً بك.. يرجى البحث عن اسمك لاستدعاء بياناتك، ثم إدخال رقم الهاتف وترتيب رغباتك.")
st.write("---")

# 2. قراءة ملف الإكسيل (قاعدة البيانات)
@st.cache_data
def load_data():
    try:
        # قراءة الملف واستبعاد أي صفوف فارغة في عمود الاسم
df = pd.read_excel("data.xlsx")
df = df.dropna(subset=['الاسم'])
        return df
    except FileNotFoundError:
        return None

df = load_data()

if df is None:
    st.error("⚠️ ملف قاعدة البيانات (جماعية.xlsx) غير موجود. يرجى رفعه بجوار ملف التطبيق.")
    st.stop()

student_names = df['الاسم'].astype(str).tolist()

# 3. القائمة المنسدلة الذكية للبحث عن الاسم
selected_name = st.selectbox("🔍 ابحث عن اسمك (اكتب أول حرفين من اسمك للبحث):", [""] + student_names)

if selected_name:
    # استخراج بيانات الطالب المختار
    student_data = df[df['الاسم'] == selected_name].iloc[0]
    
    st.success("✅ تم العثور على بياناتك بنجاح! يرجى مراجعتها أدناه.")
    
    # 4. عرض البيانات الأساسية (للقراءة فقط - لمنع التلاعب)
    st.markdown("### 📋 بياناتك الأكاديمية (معتمدة من الكنترول)")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.text_input("المجموع الكلي", value=str(student_data['المجموع']), disabled=True)
    with col2:
        st.text_input("النسبة المئوية (%)", value=str(student_data['النسبة']), disabled=True)
    with col3:
        st.text_input("التقدير", value=str(student_data['التقدير']), disabled=True)
        
    st.markdown("---")
    
    # 5. استكمال التسجيل
    st.markdown("### 📱 استكمال بيانات الاتصال والرغبات")
    phone = st.text_input("رقم الهاتف (للتواصل واتساب):", max_chars=11)
    
    options = ["كرة القدم", "الكرة الطائرة", "كرة السلة", "كرة اليد"]
    
    r1 = st.selectbox("الرغبة الأولى:", ["اختر..."] + options)
    r2 = st.selectbox("الرغبة الثانية:", ["اختر..."] + options)
    r3 = st.selectbox("الرغبة الثالثة:", ["اختر..."] + options)
    r4 = st.selectbox("الرغبة الرابعة:", ["اختر..."] + options)
    
    if st.button("حفظ الرغبات نهائياً"):
        # التحقق من صحة الإدخالات
        selections = [r1, r2, r3, r4]
        if "اختر..." in selections:
            st.error("⚠️ يرجى ترتيب جميع الرغبات الأربعة.")
        elif len(set(selections)) < 4:
            st.error("⚠️ لا يمكن تكرار نفس التخصص في أكثر من رغبة. يرجى اختيار تخصص مختلف لكل رغبة.")
        elif not phone or len(phone) < 10:
            st.error("⚠️ يرجى إدخال رقم هاتف صحيح ومكتمل.")
        else:
            # رسالة نجاح مبدئية (سيتم لاحقاً ربطها بقاعدة الحفظ النهائية)
            st.success(f"🎉 تم تسجيل رغباتك بنجاح يا {selected_name}!")
