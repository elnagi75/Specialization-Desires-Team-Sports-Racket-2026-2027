import streamlit as st
import pandas as pd
from datetime import date
import os

# 1. إعدادات الصفحة والتصميم الفاخر
st.set_page_config(page_title="منصة تسجيل الرغبات - الرياضات الجماعية", layout="centered", page_icon="🎓")

# تنسيقات CSS المتقدمة للإبهار البصري، ضبط اتجاه الكتابة، وتوسيع الخطوط وتلوينها
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: RTL;
        text-align: right;
    }
    
    /* تنسيق العنوان الرئيسي */
    .main-title {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    
    .main-title h1 {
        font-size: 28px;
        font-weight: 900;
        margin-bottom: 10px;
        color: #ffffff;
    }
    
    .main-title p {
        font-size: 16px;
        color: #e0e0e0;
        margin: 0;
    }

    /* صندوق التعليمات المتميز */
    .instructions-box {
        background-color: #f8f9fa;
        border-right: 6px solid #1e3c72;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }
    
    .instructions-box h3 {
        color: #1e3c72;
        font-weight: 700;
        margin-top: 0;
    }
    
    .instructions-box ul {
        padding-right: 20px;
    }
    
    .instructions-box li {
        font-size: 15px;
        color: #333;
        margin-bottom: 8px;
        font-weight: 600;
    }

    /* تنسيق الحقول والقوائم */
    .stSelectbox label, .stTextInput label {
        font-weight: 700 !important;
        color: #2c3e50 !important;
        font-size: 16px !important;
    }
    
    /* زر الحفظ البارز */
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

# 2. بوابة دخول الإدارة (مخفية في القائمة الجانبية)
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
    try:
        st.image("fac_logo.png", use_column_width=True)
    except:
        pass

with col_title:
    st.markdown("""
        <div class="main-title">
            <h1>منصة تسجيل الرغبات - الرياضات الجماعية</h1>
            <p>ألعاب المضرب والتخصصات الأكاديمية (2026 - 2027)</p>
        </div>
    """, unsafe_allow_html=True)

with col_logo2:
    try:
        st.image("uni_logo.png", use_column_width=True)
    except:
        pass

# 4. صندوق التعليمات الفاخر
st.markdown("""
<div class="instructions-box">
    <h3>📌 تعليمات هامة للتسجيل:</h3>
    <ul>
        <li><b>استدعاء البيانات:</b> ابدأ بكتابة أول حرفين من اسمك في خانة البحث أدناه، وقم باختياره لتظهر درجاتك المعتمدة.</li>
        <li><b>البيانات الشخصية:</b> يُشترط إدخال (القم القومي 14 رقماً)، و(رقم الواتساب) بشكل صحيح.</li>
        <li><b>ترتيب الرغبات:</b> يجب ترتيب <b>جميع التخصصات السبعة</b> المتاحة (كرة القدم، كرة اليد، الكرة الطائرة، كرة السلة، الهوكي، التنس الأرضي، اسكواش) دون تكرار.</li>
        <li><b>مواعيد التسجيل:</b> ⏳ يفتح باب التسجيل من يوم <b>الأحد 9-8-2026</b> ويُغلق آلياً يوم <b>السبت 22-8-2026</b>.</li>
        <li><b>التخلف عن التسجيل:</b> ⚠️ الطالب الذي لا يسجل رغباته خلال هذه الفترة، سيتم توزيعه آلياً وفقاً للأماكن الشاغرة.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# 5. التوقيت الزمني للمنصة (مضبوط مؤقتاً لليوم ليفتح معك فوراً للتجربة)
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
    
    # 8. استكمال التسجيل
    st.markdown("### 📱 استكمال البيانات الشخصية وترتيب الرغبات (7 رغبات)")
    nat_id = st.text_input("الرقم القومي (14 رقماً):", max_chars=14, placeholder="أدخل الرقم القومي المدون ببطاقة الرقم القومي")
    phone = st.text_input("رقم الهاتف (واتساب):", max_chars=11, placeholder="01xxxxxxxx0")
    
    # التخصصات السبعة
    options = ["كرة القدم", "كرة اليد", "الكرة الطائرة", "كرة السلة", "الهوكي", "التنس الأرضي", "اسكواش"]
    
    st.markdown("---")
    st.markdown("#### 🎯 حدد رغباتك بترتيب الأولوية من الأولى إلى السابعة:")
    
    c1, c2 = st.columns(2)
    with c1:
        r1 = st.selectbox("الرغبة الأولى:", ["اختر التخصص..."] + options)
        r2 = st.selectbox("الرغبة الثانية:", ["اختر التخصص..."] + options)
        r3 = st.selectbox("الرغبة الثالثة:", ["اختر التخصص..."] + options)
        r4 = st.selectbox("الرغبة الرابعة:", ["اختر التخصص..."] + options)
    with c2:
        r5 = st.selectbox("الرغبة الخامسة:", ["اختر التخصص..."] + options)
        r6 = st.selectbox("الرغبة السادسة:", ["اختر التخصص..."] + options)
        r7 = st.selectbox("الرغبة السابعة:", ["اختر التخصص..."] + options)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("💾 حفظ وتأكيد الرغبات نهائياً"):
        selections = [r1, r2, r3, r4, r5, r6, r7]
        
        # الفلترة والتحقق
        if "اختر التخصص..." in selections:
            st.error("⚠️ يرجى استكمال ترتيب جميع الرغبات السبعة قبل الحفظ.")
        elif len(set(selections)) < 7:
            st.error("⚠️ لا يمكن تكرار نفس التخصص في رغبتين مختلفتين. يرجى اختيار تخصص فريد لكل رغبة.")
        elif not nat_id or len(nat_id) < 14:
            st.error("⚠️ يرجى إدخال الرقم القومي المكون من 14 رقماً بشكل صحيح.")
        elif not phone or len(phone) < 10:
            st.error("⚠️ يرجى إدخال رقم هاتف صحيح ومكتمل.")
        else:
            # 9. حفظ البيانات للكنترول
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
