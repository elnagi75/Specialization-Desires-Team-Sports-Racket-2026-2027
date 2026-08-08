import streamlit as st
import pandas as pd
from datetime import date
import os

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة تسجيل الرغبات - الرياضات الجماعية", layout="centered", page_icon="🎓")

# تنسيقات CSS لضبط اتجاه الكتابة والإبهار البصري
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: RTL !important;
        text-align: right !important;
    }
    
    /* تنسيق العنوان الرئيسي */
    .main-title {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    .main-title h1 {
        font-size: 26px;
        font-weight: 900;
        margin-bottom: 5px;
        color: #ffffff;
    }
    
    .main-title p {
        font-size: 15px;
        color: #e0e0e0;
        margin: 0;
    }

    /* صندوق التعليمات */
    .instructions-box {
        background-color: #f8f9fa;
        border-right: 6px solid #1e3c72;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    
    .instructions-box h3 {
        color: #1e3c72;
        font-weight: 700;
        margin-top: 0;
    }
    
    .instructions-box li {
        font-size: 14px;
        color: #333;
        margin-bottom: 6px;
        font-weight: 600;
    }

    /* تمييز الرغبة الأولى بشكل مبهج وكبير */
    .first-choice-container {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeeba 100%);
        border: 2px dashed #ffc107;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 15px;
    }
    
    .first-choice-container label {
        font-size: 20px !important;
        font-weight: 900 !important;
        color: #856404 !important;
    }

    .stSelectbox, .stTextInput {
        text-align: right !important;
    }
    
    /* زر الحفظ */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        font-size: 18px;
        font-weight: 700;
        padding: 12px;
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# 2. بوابة دخول الإدارة في القائمة الجانبية
st.sidebar.title("👨‍💻 لوحة الكنترول والإدارة")
admin_pass = st.sidebar.text_input("أدخل كلمة المرور:", type="password")

if admin_pass == "2027":
    st.sidebar.success("تم الدخول بنجاح")
    st.title("📥 لوحة تحكم الإدارة (تحميل الرغبات)")
    st.info("هنا يتم تجميع بيانات الطلاب الذين سجلوا رغباتهم لسحبها في ملف إكسيل.")
    
    if os.path.exists("student_requests.csv"):
        df_requests = pd.read_csv("student_requests.csv")
        st.dataframe(df_requests)
        
        csv = df_requests.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 تحميل كشف الرغبات النهائي (Excel/CSV)",
            data=csv,
            file_name='student_requests.csv',
            mime='text/csv',
        )
    else:
        st.warning("لم يقم أي طالب بالتسجيل حتى الآن.")
    st.stop()

# 3. عرض الشعارات الأكاديمية والعنوان الرئيسي
col_logo1, col_title, col_logo2 = st.columns([1, 4, 1])

with col_logo1:
    if os.path.exists("fac_logo.png"):
        st.image("fac_logo.png", use_container_width=True)

with col_title:
    st.markdown("""
        <div class="main-title">
            <h1>منصة تسجيل الرغبات - الرياضات الجماعية</h1>
            <p>ألعاب المضرب والتخصصات الأكاديمية (2026 - 2027)</p>
        </div>
    """, unsafe_allow_html=True)

with col_logo2:
    if os.path.exists("uni_logo.png"):
        st.image("uni_logo.png", use_container_width=True)

# 4. صندوق التعليمات الفاخر
st.markdown("""
<div class="instructions-box">
    <h3>📌 تعليمات هامة للتسجيل:</h3>
    <ul>
        <li><b>استدعاء البيانات:</b> ابدأ بكتابة أول حرفين من اسمك في خانة البحث أدناه، وقم باختياره لتظهر درجاتك المعتمدة.</li>
        <li><b>البيانات الشخصية:</b> يُشترط إدخال (الرقم القومي 14 رقماً)، و(رقم الواتساب) بشكل صحيح.</li>
        <li><b>ترتيب الرغبات:</b> يجب ترتيب <b>جميع التخصصات السبعة</b> دون تكرار (كل تخصص يتم اختياره يختفي تلقائياً من الخيارات التالية).</li>
        <li><b>مواعيد التسجيل:</b> ⏳ يفتح باب التسجيل من يوم <b>الأحد 9-8-2026</b> ويُغلق آلياً يوم <b>السبت 22-8-2026</b>.</li>
        <li><b>التخلف عن التسجيل:</b> ⚠️ الطالب الذي لا يسجل رغباته خلال هذه الفترة، سيتم توزيعه آلياً وفقاً للأماكن الشاغرة.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# 5. التوقيت الزمني للمنصة
start_date = date(2026, 8, 8) 
end_date = date(2026, 8, 22)
today = date.today()

if today < start_date:
    st.warning("⏳ المنصة مغلقة حالياً. سيتم فتح باب التسجيل غداً الأحد 9-8-2026.")
    st.stop()
elif today > end_date:
    st.error("❌ انتهى وقت التسجيل. تم إغلاق المنصة.")
    st.stop()

# 6. قراءة قاعدة البيانات الأساسية للإكسيل
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("data.xlsx")
        df = df.dropna(subset=['الاسم'])
        return df
    except FileNotFoundError:
        return None

df = load_data()

if df is None:
    st.error("⚠️ ملف قاعدة البيانات (data.xlsx) غير موجود في المستودع.")
    st.stop()

student_names = df['الاسم'].astype(str).tolist()

# 7. البحث الذكي المنسدل
selected_name = st.selectbox("🔍 ابحث عن اسمك (اكتب أول حرفين من اسمك للبحث):", ["اختر اسم الطالب من هنا..."] + student_names)

if selected_name and selected_name != "اختر اسم الطالب من هنا...":
    student_data = df[df['الاسم'] == selected_name].iloc[0]
    st.success(f"✅ أهلاً بك يا {selected_name}.. تم العثور على بياناتك بنجاح!")
    
    # تنسيق عرض الدرجات (مغلقة)
    colA, colB, colC = st.columns(3)
    with colA:
        st.text_input("المجموع الكلي", value=str(student_data['المجموع']), disabled=True)
    with colB:
        st.text_input("النسبة المئوية (%)", value=str(student_data['النسبة']), disabled=True)
    with colC:
        st.text_input("التقدير الأكاديمي", value=str(student_data['التقدير']), disabled=True)
        
    st.markdown("---")
    
    # 8. استكمال البيانات الشخصية
    st.markdown("### 📱 استكمال البيانات الشخصية وترتيب الرغبات")
    nat_id = st.text_input("الرقم القومي (14 رقماً):", max_chars=14, placeholder="أدخل الرقم القومي المدون ببطاقة الرقم القومي")
    phone = st.text_input("رقم الهاتف (واتساب):", max_chars=11, placeholder="01xxxxxxxx0")
    
    # التخصصات الأساسية
    all_options = ["كرة القدم", "كرة اليد", "الكرة الطائرة", "كرة السلة", "الهوكي", "التنس الأرضي", "اسكواش"]
    
    st.markdown("---")
    st.markdown("#### 🎯 حدد رغباتك بترتيب الأولوية (من الأولى إلى السابعة):")
    
    # نظام ديناميكي لمنع تكرار الرغبات وتكبير الرغبة الأولى
    st.markdown('<div class="first-choice-container">', unsafe_allow_html=True)
    r1 = st.selectbox("⭐ الرغبة الأولى (الأساسية):", ["اختر التخصص..."] + all_options)
    st.markdown('</div>', unsafe_allow_html=True)
    
    opts_after_r1 = [opt for opt in all_options if opt != r1]
    r2 = st.selectbox("الرغبة الثانية:", ["اختر التخصص..."] + opts_after_r1)
    
    opts_after_r2 = [opt for opt in opts_after_r1 if opt != r2]
    r3 = st.selectbox("الرغبة الثالثة:", ["اختر التخصص..."] + opts_after_r2)
    
    opts_after_r3 = [opt for opt in opts_after_r2 if opt != r3]
    r4 = st.selectbox("الرغبة الرابعة:", ["اختر التخصص..."] + opts_after_r3)
    
    opts_after_r4 = [opt for opt in opts_after_r3 if opt != r4]
    r5 = st.selectbox("الرغبة الخامسة:", ["اختر التخصص..."] + opts_after_r4)
    
    opts_after_r5 = [opt for opt in opts_after_r4 if opt != r5]
    r6 = st.selectbox("الرغبة السادسة:", ["اختر التخصص..."] + opts_after_r5)
    
    opts_after_r6 = [opt for opt in opts_after_r5 if opt != r6]
    r7 = st.selectbox("الرغبة السابعة:", ["اختر التخصص..."] + opts_after_r6)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("💾 حفظ وتأكيد الرغبات نهائياً"):
        selections = [r1, r2, r3, r4, r5, r6, r7]
        
        if "اختر التخصص..." in selections:
            st.error("⚠️ يرجى استكمال ترتيب جميع الرغبات السبعة قبل الحفظ.")
        elif len(set(selections)) < 7:
            st.error("⚠️ لا يمكن تكرار نفس التخصص في رغبتين مختلفتين.")
        elif not nat_id or len(nat_id) < 14:
            st.error("⚠️ يرجى إدخال الرقم القومي المكون من 14 رقماً بشكل صحيح.")
        elif not phone or len(phone) < 10:
            st.error("⚠️ يرجى إدخال رقم هاتف صحيح ومكتمل.")
        else:
            new_data = pd.DataFrame({
                "الاسم": [selected_name],
                "الرقم القومي": [nat_id],
                "رقم الهاتف": [phone],
                "المجموع": [student_data['المجموع']],
                "النسبة": [student_data['النسبة']],
                "التقدير": [student_data['التقدير']],
                "رغبة 1": [r1], "رغبة 2": [r2], "رغبة 3": [r3],
                "رغبة 4": [r4], "رغبة 5": [r5], "رغبة 6": [r6], "رغبة 7": [r7]
            })
            
            if os.path.exists("student_requests.csv"):
                df_requests = pd.read_csv("student_requests.csv")
                df_requests = df_requests[df_requests['الاسم'] != selected_name]
                df_requests = pd.concat([df_requests, new_data], ignore_index=True)
            else:
                df_requests = new_data
                
            df_requests.to_csv("student_requests.csv", index=False)
            
            st.balloons()
            st.success(f"🎉 مبروك يا {selected_name}! تم حفظ رغباتك السبعة بنجاح في قاعدة البيانات الرسمية.")
