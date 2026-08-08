import streamlit as st
import pandas as pd
from datetime import date
import os

# 1. إعدادات الصفحة
st.set_page_config(page_title="تسجيل الرغبات - الرياضات الجماعية", layout="centered", page_icon="📝")

# توجيه النص من اليمين لليسار
st.markdown("""
    <style>
    body, p, h1, h2, h3, h4, h5, h6, label { direction: RTL !important; text-align: right !important; font-family: 'Arial', sans-serif; }
    .stSelectbox>label, .stTextInput>label { display: flex; justify-content: right; }
    </style>
""", unsafe_allow_html=True)

# 2. بوابة دخول الإدارة (مخفية في القائمة الجانبية)
st.sidebar.title("👨‍💻 لوحة الكنترول والإدارة")
admin_pass = st.sidebar.text_input("أدخل كلمة المرور:", type="password")

if admin_pass == "2027": # يمكنك تغيير كلمة المرور "2027" لأي رقم تريده
    st.sidebar.success("تم الدخول بنجاح")
    st.title("📥 لوحة تحكم الإدارة (تحميل الرغبات)")
    st.info("هنا يتم تجميع بيانات الطلاب الذين سجلوا رغباتهم لسحبها في ملف إكسيل.")
    
    # قراءة الملف الذي يحفظ الرغبات (إن وجد)
    if os.path.exists("student_requests.csv"):
        df_requests = pd.read_csv("student_requests.csv")
        st.dataframe(df_requests)
        
        # زر تحميل كشف الرغبات
        csv = df_requests.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="تحميل كشف الرغبات النهائي (Excel/CSV)",
            data=csv,
            file_name='student_requests.csv',
            mime='text/csv',
        )
    else:
        st.warning("لم يقم أي طالب بالتسجيل حتى الآن.")
    st.stop() # إيقاف عرض باقي الصفحة للمدير

# 3. واجهة الطالب الأساسية
# إضافة الشعارات الأكاديمية
col1, col2, col3 = st.columns([1, 2, 1])
try:
    with col1:
        st.image("fac_logo.png", use_column_width=True)
    with col3:
        st.image("uni_logo.png", use_column_width=True)
except:
    pass 

st.title("منصة تسجيل الرغبات - الرياضات الجماعية وألعاب المضرب (2027-2026)")

# 4. التعليمات المعتمدة
st.markdown("""
**مرحباً بك.. يرجى البحث عن اسمك لاستدعاء بياناتك، ثم إدخال الرقم القومي ورقم الهاتف (واتساب) وترتيب رغباتك.**

**📌 تعليمات هامة للتسجيل:**
1. **استدعاء البيانات:** ابدأ بكتابة أول حرفين من اسمك في خانة البحث، وقم باختياره من القائمة لتظهر درجاتك المعتمدة.
2. **البيانات الشخصية:** يُشترط إدخال (الرقم القومي 14 رقماً)، و(رقم الواتساب) بشكل صحيح.
3. **ترتيب الرغبات:** يجب ترتيب **جميع التخصصات السبعة** المتاحة دون تكرار.
4. **مواعيد التسجيل:** ⏳ يفتح باب التسجيل من يوم **الأحد 9-8-2026** ويُغلق آلياً يوم **السبت 22-8-2026**.
5. **التخلف عن التسجيل:** ⚠️ الطالب الذي لا يسجل رغباته خلال هذه الفترة، سيتم توزيعه آلياً وفقاً للأماكن الشاغرة.
---
""")

# 5. التوقيت الزمني للمنصة
# ملاحظة: تم ضبط البداية على يوم 8 مؤقتاً لتتمكن من التجربة اليوم، يمكنك تغيير الـ 8 إلى 9 لاحقاً
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
    st.error("⚠️ ملف قاعدة البيانات (data.xlsx) غير موجود.")
    st.stop()

student_names = df['الاسم'].astype(str).tolist()

# 7. البحث الذكي
selected_name = st.selectbox("🔍 ابحث عن اسمك (اكتب أول حرفين من اسمك للبحث):", [""] + student_names)

if selected_name:
    student_data = df[df['الاسم'] == selected_name].iloc[0]
    st.success("✅ تم العثور على بياناتك بنجاح! يرجى مراجعتها.")
    
    # تنسيق عرض الدرجات (مغلقة)
    colA, colB, colC = st.columns(3)
    with colA:
        st.text_input("المجموع الكلي", value=str(student_data['المجموع']), disabled=True)
    with colB:
        st.text_input("النسبة المئوية (%)", value=str(student_data['النسبة']), disabled=True)
    with colC:
        st.text_input("التقدير", value=str(student_data['التقدير']), disabled=True)
        
    st.write("---")
    
    # 8. استكمال التسجيل
    st.markdown("### 📱 البيانات الشخصية والرغبات")
    nat_id = st.text_input("الرقم القومي (14 رقماً):", max_chars=14)
    phone = st.text_input("رقم الهاتف (واتساب):", max_chars=11)
    
    # التخصصات السبعة
    options = ["كرة القدم", "كرة اليد", "الكرة الطائرة", "كرة السلة", "الهوكي", "التنس الأرضي", "اسكواش"]
    
    st.markdown("**قم باختيار التخصصات الـ 7 بالترتيب حسب رغبتك:**")
    r1 = st.selectbox("الرغبة الأولى:", ["اختر..."] + options)
    r2 = st.selectbox("الرغبة الثانية:", ["اختر..."] + options)
    r3 = st.selectbox("الرغبة الثالثة:", ["اختر..."] + options)
    r4 = st.selectbox("الرغبة الرابعة:", ["اختر..."] + options)
    r5 = st.selectbox("الرغبة الخامسة:", ["اختر..."] + options)
    r6 = st.selectbox("الرغبة السادسة:", ["اختر..."] + options)
    r7 = st.selectbox("الرغبة السابعة:", ["اختر..."] + options)
    
    if st.button("حفظ الرغبات نهائياً"):
        selections = [r1, r2, r3, r4, r5, r6, r7]
        
        # الفلترة والتأكد من صحة البيانات
        if "اختر..." in selections:
            st.error("⚠️ يرجى ترتيب جميع الرغبات السبعة قبل الحفظ.")
        elif len(set(selections)) < 7:
            st.error("⚠️ لا يمكن تكرار نفس التخصص. يرجى اختيار تخصص مختلف لكل رغبة.")
        elif not nat_id or len(nat_id) < 14:
            st.error("⚠️ يرجى إدخال الرقم القومي المكون من 14 رقماً بشكل صحيح.")
        elif not phone or len(phone) < 10:
            st.error("⚠️ يرجى إدخال رقم هاتف صحيح.")
        else:
            # 9. حفظ البيانات في ملف جديد للكنترول
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
            
            # إضافة الطالب الجديد لقاعدة الحفظ
            if os.path.exists("student_requests.csv"):
                df_requests = pd.read_csv("student_requests.csv")
                # مسح تسجيله القديم لو أراد التعديل خلال فترة التسجيل
                df_requests = df_requests[df_requests['الاسم'] != selected_name]
                df_requests = pd.concat([df_requests, new_data], ignore_index=True)
            else:
                df_requests = new_data
                
            df_requests.to_csv("student_requests.csv", index=False)
            
            st.success(f"🎉 تم تسجيل رغباتك بنجاح يا {selected_name}! يمكنك إغلاق الموقع الآن.")
