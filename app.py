import streamlit as st
import pandas as pd
from datetime import date
import os

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة تسجيل الرغبات - الرياضات الجماعية", layout="centered", page_icon="🎓")

# تنسيقات CSS المتقدمة لضبط العنوان، النصوص، والزر الأحمر القاني
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
        <li><b>استدعاء البيانات:</b> ابدأ بكتابة أول حرفين من اسمك في خانة البحث، وقم باختياره لتظهر درجاتك المعتمدة.</li>
        <li><b>الخطوة البينية الأمنية:</b> أدخل (الرقم القومي 14 رقماً) و(رقم الواتساب) واضغط على زر التحقق لفتح صفحة رغباتك.</li>
        <li><b>ترتيب الرغبات:</b> يجب ترتيب <b>جميع التخصصات السبعة</b> دون تكرار (كل تخصص يتم اختياره يختفي تلقائياً من الخيارات التالية).</li>
        <li><b>مواعيد وقابلية التعديل:</b> ⏳ يفتح باب التسجيل والتعديل من يوم <b>الأحد 9-8-2026</b> حتى يوم <b>السبت 22-8-2026</b>.</li>
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
    
    # التحقق من وجود تسجيل سابق لاسترجاع البيانات
    saved_record = None
    if os.path.exists("student_requests.csv"):
        df_reqs = pd.read_csv("student_requests.csv")
        match = df_reqs[df_reqs['الاسم'] == selected_name]
        if not match.empty:
            saved_record = match.iloc[0]

    st.success(f"✅ أهلاً بك يا {selected_name}.. تم العثور على بياناتك بنجاح!")
    
    # عرض الدرجات (مغلقة)
    colA, colB, colC = st.columns(3)
    with colA:
        st.text_input("المجموع الكلي", value=str(student_data['المجموع']), disabled=True)
    with colB:
        st.text_input("النسبة المئوية (%)", value=str(student_data['النسبة']), disabled=True)
    with colC:
        st.text_input("التقدير الأكاديمي", value=str(student_data['التقدير']), disabled=True)
        
    st.markdown("---")
    
    # الخطوة البينية: إدخال الرقم القومي ورقم الهاتف أولاً لفتح الرغبات
    st.markdown("### 📱 الخطوة الأمنية: إدخال بيانات التوثيق")
    
    default_id = str(saved_record['الرقم القومي']) if saved_record is not None else ""
    default_phone = str(saved_record['رقم الهاتف']) if saved_record is not None else ""
    
    nat_id = st.text_input("الرقم القومي (14 رقماً):", value=default_id, max_chars=14, placeholder="أدخل الرقم القومي المدون ببطاقة الرقم القومي")
    phone = st.text_input("رقم الهاتف (واتساب):", value=default_phone, max_chars=11, placeholder="01xxxxxxxx0")
    
    # زر أو شرط لفتح الرغبات
    if len(nat_id) == 14 and len(phone) >= 10:
        if saved_record is not None:
            st.info("💡 تم العثور على رغباتك المسجلة مسبقاً. يمكنك تعديلها وإعادة الحفظ أدناه.")
        else:
            st.success("🔓 تم التحقق من البيانات بنجاح! تم فتح خانات ترتيب الرغبات أدناه:")
            
        st.markdown("---")
        st.markdown("#### 🎯 حدد رغباتك بترتيب الأولوية (من الأولى إلى السابعة):")
        
        all_options = ["كرة القدم", "كرة اليد", "الكرة الطائرة", "كرة السلة", "الهوكي", "التنس الأرضي", "اسكواش"]
        
        def get_saved_choice(idx):
            if saved_record is not None:
                return saved_record.get(f'رغبة {idx}', "اختر التخصص...")
            return "اختر التخصص..."

        def get_index(val, opts):
            if val in opts:
                return opts.index(val) + 1
            return 0

        # الرغبة الأولى المميزة
        st.markdown('<div class="first-choice-container">', unsafe_allow_html=True)
        r1_opts = ["اختر التخصص..."] + all_options
        r1_val = get_saved_choice(1)
        r1 = st.selectbox("⭐ الرغبة الأولى (الأساسية):", r1_opts, index=get_index(r1_val, all_options))
        st.markdown('</div>', unsafe_allow_html=True)
        
        # الرغبات الباقية مع منع التكرار الديناميكي
        opts_after_r1 = [opt for opt in all_options if opt != r1]
        r2 = st.selectbox("الرغبة الثانية:", ["اختر التخصص..."] + opts_after_r1, index=get_index(get_saved_choice(2), opts_after_r1))
        
        opts_after_r2 = [opt for opt in opts_after_r1 if opt != r2]
        r3 = st.selectbox("الرغبة الثالثة:", ["اختر التخصص..."] + opts_after_r2, index=get_index(get_saved_choice(3), opts_after_r2))
        
        opts_after_r3 = [opt for opt in opts_after_r2 if opt != r3]
        r4 = st.selectbox("الرغبة الرابعة:", ["اختر التخصص..."] + opts_after_r3, index=get_index(get_saved_choice(4), opts_after_r3))
        
        opts_after_r4 = [opt for opt in opts_after_r3 if opt != r4]
        r5 = st.selectbox("الرغبة الخامسة:", ["اختر التخصص..."] + opts_after_r4, index=get_index(get_saved_choice(5), opts_after_r4))
        
        opts_after_r5 = [opt for opt in opts_after_r4 if opt != r5]
        r6 = st.selectbox("الرغبة السادسة:", ["اختر التخصص..."] + opts_after_r5, index=get_index(get_saved_choice(6), opts_after_r5))
        
        opts_after_r6 = [opt for opt in opts_after_r5 if opt != r6]
        r7 = st.selectbox("الرغبة السابعة:", ["اختر التخصص..."] + opts_after_r6, index=get_index(get_saved_choice(7), opts_after_r6))
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("💾 حفظ وتأكيد الرغبات نهائياً"):
            selections = [r1, r2, r3, r4, r5, r6, r7]
            
            if "اختر التخصص..." in selections:
                st.error("⚠️ يرجى استكمال ترتيب جميع الرغبات السبعة قبل الحفظ.")
            elif len(set(selections)) < 7:
                st.error("⚠️ لا يمكن تكرار نفس التخصص في رغبتين مختلفتين.")
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
                st.success(f"🎉 مبروك يا {selected_name}! تم حفظ وتأكيد رغباتك السبعة بنجاح.")
    else:
        st.warning("🔒 يرجى إدخال الرقم القومي المكون من 14 رقماً ورقم الهاتف (واتساب) بشكل صحيح لفتح خانات ترتيب الرغبات.")
