import streamlit as st
import pandas as pd
from datetime import date
import os

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة تسجيل الرغبات - الرياضات الجماعية", layout="centered", page_icon="🎓")

# تنسيقات CSS لضبط العنوان (توسيط ونمط موحد كبير)، ونصوص المنصة (يمين)، والزر الأحمر القاني
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
    }
    
    /* تنسيق العنوان الرئيسي: توسيط وبنفس الحجم والنمط الكبير */
    .main-title {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 25px 20px;
        border-radius: 15px;
        text-align: center !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    
    .main-title h1 {
        font-size: 24px !important;
        font-weight: 900 !important;
        color: #ffffff !important;
        line-height: 1.5;
        margin: 0 !important;
        text-align: center !important;
    }

    /* اتجاه وباقي نصوص المنصة ناحية اليمين */
    .stMarkdown, p, li, label, .stTextInput, .stSelectbox {
        direction: RTL !important;
        text-align: right !important;
    }

    /* صندوق التعليمات */
    .instructions-box {
        background-color: #f8f9fa;
        border-right: 6px solid #1e3c72;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 25px;
        direction: RTL !important;
        text-align: right !important;
    }
    
    .instructions-box h3 {
        color: #1e3c72;
        font-weight: 700;
        margin-top: 0;
        text-align: right !important;
    }
    
    .instructions-box li {
        font-size: 15px;
        color: #333;
        margin-bottom: 8px;
        font-weight: 600;
        text-align: right !important;
    }

    /* تمييز الرغبة الأولى بشكل مبهج وكبير */
    .first-choice-container {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeeba 100%);
        border: 2px dashed #ffc107;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 15px;
        direction: RTL !important;
    }
    
    .first-choice-container label {
        font-size: 20px !important;
        font-weight: 900 !important;
        color: #856404 !important;
        text-align: right !important;
    }

    /* تكبير وتظبيط خطوط الرغبات وباقي الحقول */
    .stSelectbox label, .stTextInput label {
        font-size: 17px !important;
        font-weight: 700 !important;
        color: #2c3e50 !important;
        text-align: right !important;
    }
    
    /* زر الحفظ والتأكيد بلون أحمر قاني فخم */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #8B0000 0%, #B22222 100%) !important;
        color: white !important;
        font-size: 19px !important;
        font-weight: 700 !important;
        padding: 14px !important;
        border-radius: 10px !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(139, 0, 0, 0.3) !important;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #A52A2A 0%, #DC143C 100%) !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(139, 0, 0, 0.4) !important;
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
            <h1>منصة تسجيل الرغبات - الرياضات الجماعية وألعاب المضرب والتخصصات الأكاديمية - (2026 - 2027)</h1>
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
        <li><b>البيانات الشخصية:</b> يُشترط إدخال (الرقم القومي 14 رقماً)، و(رقم الواتساب) بنفسك.</li>
        <li><b>ترتيب الرغبات:</b> يجب ترتيب <b>جميع التخصصات السبعة</b> دون تكرار (كل تخصص يتم اختياره يختفي تلقائياً من الخيارات التالية).</li>
        <li><b>مواعيد وقابلية التعديل:</b> ⏳ يفتح باب التسجيل والتعديل من يوم <b>الأحد 9-8-2026</b> حتى يوم <b>السبت 22-8-2026</b> (يمكنك تعديل رغباتك في أي وقت خلال هذه الفترة).</li>
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
    
    # فحص ما إذا كان الطالب قد سجل مسبقاً لاسترجاع بياناته ورغباته القديمة للتعديل
    prev_nat_id = ""
    prev_phone = ""
    saved_choices = {}
    
    if os.path.exists("student_requests.csv"):
        df_reqs = pd.read_csv("student_requests.csv")
        student_record = df_reqs[df_reqs['الاسم'] == selected_name]
        if not student_record.empty:
            prev_nat_id = str(student_record.iloc[0]['الرقم القومي'])
            prev_phone = str(student_record.iloc[0]['رقم الهاتف'])
            for i in range(1, 8):
                saved_choices[f'رغبة {i}'] = student_record.iloc[0][f'رغبة {i}']
            st.info("💡 لقد قمت بتسجيل رغباتك مسبقاً. يمكنك تعديلها وإعادة الحفظ خلال فترة التسجيل المفتوحة.")

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
    nat_id = st.text_input("الرقم القومي (14 رقماً):", value=prev_nat_id, max_chars=14, placeholder="أدخل الرقم القومي المدون ببطاقة الرقم القومي")
    phone = st.text_input("رقم الهاتف (واتساب):", value=prev_phone, max_chars=11, placeholder="01xxxxxxxx0")
    
    # التخصصات الأساسية
    all_options = ["كرة القدم", "كرة اليد", "الكرة الطائرة", "كرة السلة", "الهوكي", "التنس الأرضي", "اسكواش"]
    
    st.markdown("---")
    st.markdown("#### 🎯 حدد رغباتك بترتيب الأولوية (من الأولى إلى السابعة):")
    
    # دالة مساعدة لتحديد الفهرس الافتراضي للقائمة المنسدلة في حالة التعديل
    def get_index(saved_val, options_list):
        if saved_val in options_list:
            return options_list.index(saved_val) + 1
        return 0

    # الرغبة الأولى المميزة
    st.markdown('<div class="first-choice-container">', unsafe_allow_html=True)
    default_r1 = saved_choices.get('رغبة 1', "اختر التخصص...")
    r1_options = ["اختر التخصص..."] + all_options
    r1_idx = get_index(default_r1, all_options)
    r1 = st.selectbox("⭐ الرغبة الأولى (الأساسية):", r1_options, index=r1_idx)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # الرغبة الثانية
    opts_after_r1 = [opt for opt in all_options if opt != r1]
    default_r2 = saved_choices.get('رغبة 2', "اختر التخصص...")
    r2_options = ["اختر التخصص..."] + opts_after_r1
    r2_idx = get_index(default_r2, opts_after_r1)
    r2 = st.selectbox("الرغبة الثانية:", r2_options, index=r2_idx)
    
    # الرغبة الثالثة
    opts_after_r2 = [opt for opt in opts_after_r1 if opt != r2]
    default_r3 = saved_choices.get('رغبة 3', "اختر التخصص...")
    r3_options = ["اختر التخصص..."] + opts_after_r2
    r3_idx = get_index(default_r3, opts_after_r2)
    r3 = st.selectbox("الرغبة الثالثة:", r3_options, index=r3_idx)
    
    # الرغبة الرابعة
    opts_after_r3 = [opt for opt in opts_after_r2 if opt != r3]
    default_r4 = saved_choices.get('رغبة 4', "اختر التخصص...")
    r4_options = ["اختر التخصص..."] + opts_after_r3
    r4_idx = get_index(default_r4, opts_after_r3)
    r4 = st.selectbox("الرغبة الرابعة:", r4_options, index=r4_idx)
    
    # الرغبة الخامسة
    opts_after_r4 = [opt for opt in opts_after_r3 if opt != r4]
    default_r5 = saved_choices.get('رغبة 5', "اختر التخصص...")
    r5_options = ["اختر التخصص..."] + opts_after_r4
    r5_idx = get_index(default_r5, opts_after_r4)
    r5 = st.selectbox("الرغبة الخامسة:", r5_options, index=r5_idx)
    
    # الرغبة السادسة
    opts_after_r5 = [opt for opt in opts_after_r4 if opt != r5]
    default_r6 = saved_choices.get('رغبة 6', "اختر التخصص...")
    r6_options = ["اختر التخصص..."] + opts_after_r5
    r6_idx = get_index(default_r6, opts_after_r5)
    r6 = st.selectbox("الرغبة السادسة:", r6_options, index=r6_idx)
    
    # الرغبة السابعة
    opts_after_r6 = [opt for opt in opts_after_r5 if opt != r6]
    default_r7 = saved_choices.get('رغبة 7', "اختر التخصص...")
    r7_options = ["اختر التخصص..."] + opts_after_r6
    r7_idx = get_index(default_r7, opts_after_r6)
    r7 = st.selectbox("الرغبة السابعة:", r7_options, index=r7_idx)
    
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
            st.success(f"🎉 مبروك يا {selected_name}! تم حفظ/تحديث رغباتك السبعة بنجاح في قاعدة البيانات الرسمية.")
