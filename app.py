import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from datetime import date
import os
import io

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة تسجيل الرغبات - الرياضات الجماعية وألعاب المضرب", layout="centered", page_icon="🎓")

# تنسيقات CSS العامة للمنصة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
    }
    
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
        font-size: 22px !important;
        font-weight: 900 !important;
        color: #ffffff !important;
        line-height: 1.5;
        margin: 0 !important;
        text-align: center !important;
    }

    .stMarkdown, p, li, label, .stTextInput, .stSelectbox {
        direction: RTL !important;
        text-align: right !important;
    }

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

    .stSelectbox label, .stTextInput label {
        font-size: 17px !important;
        font-weight: 700 !important;
        color: #2c3e50 !important;
        text-align: right !important;
    }
    
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

# 2. بوابة دخول الإدارة في القائمة الجانبية (المحرك الشامل)
st.sidebar.title("👨‍💻 لوحة الكنترول والإدارة")
admin_pass = st.sidebar.text_input("أدخل كلمة المرور:", type="password")

if admin_pass == "2027":
    st.sidebar.success("تم الدخول بنجاح")
    st.title("📥 لوحة تحكم الكنترول المركزية")
    
    tab1, tab2 = st.tabs(["📥 كشف الرغبات الخام", "⚙️ محرك التنسيق والإخراج الذكي"])
    
    with tab1:
        st.info("هنا يتم تجميع بيانات الطلاب الذين سجلوا رغباتهم، ويمكنك تحميل الكشف الخام.")
        if os.path.exists("student_requests.xlsx"):
            df_requests = pd.read_excel("student_requests.xlsx", dtype=str)
            st.dataframe(df_requests)
            
            with open("student_requests.xlsx", "rb") as f:
                st.download_button(
                    label="📥 تحميل كشف الرغبات الخام (Excel)",
                    data=f,
                    file_name='student_requests_raw.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                )
        else:
            st.warning("لم يقم أي طالب بالتسجيل حتى الآن.")
            
    with tab2:
        st.markdown("### 🎯 إعداد السعة الاستيعابية للتخصصات")
        st.write("أدخل العدد المطلوب لكل تخصص لبدء الفرز والتوزيع وإخراج الكشوفات النهائية المنسقة:")
        
        col1, col2, col3, col4 = st.columns(4)
        cap_football = col1.number_input("كرة القدم", min_value=0, value=60)
        cap_handball = col2.number_input("كرة اليد", min_value=0, value=50)
        cap_volleyball = col3.number_input("الكرة الطائرة", min_value=0, value=50)
        cap_basketball = col4.number_input("كرة السلة", min_value=0, value=45)
        
        col5, col6, col7, col8 = st.columns(4)
        cap_hockey = col5.number_input("الهوكي", min_value=0, value=40)
        cap_tennis = col6.number_input("التنس الأرضي", min_value=0, value=45)
        cap_squash = col7.number_input("اسكواش", min_value=0, value=40)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("⚙️ إجراء التنسيق واستخراج كشوفات الكنترول"):
            if os.path.exists("student_requests.xlsx"):
                df_req = pd.read_excel("student_requests.xlsx", dtype=str)
                df_req['المجموع'] = pd.to_numeric(df_req['المجموع'], errors='coerce').fillna(0)
                df_sorted = df_req.sort_values(by='المجموع', ascending=False).reset_index(drop=True)
                
                capacities = {
                    'كرة القدم': cap_football,
                    'كرة اليد': cap_handball,
                    'الكرة الطائرة': cap_volleyball,
                    'كرة السلة': cap_basketball,
                    'الهوكي': cap_hockey,
                    'التنس الأرضي': cap_tennis,
                    'اسكواش': cap_squash
                }
                
                allocations = []
                current_capacity = {k: 0 for k in capacities.keys()}
                
                for index, row in df_sorted.iterrows():
                    assigned = False
                    for i in range(1, 8):
                        choice = row.get(f'رغبة {i}')
                        if pd.isna(choice):
                            continue
                        
                        if choice in current_capacity and current_capacity[choice] < capacities[choice]:
                            allocations.append(choice)
                            current_capacity[choice] += 1
                            assigned = True
                            break
                            
                    if not assigned:
                        allocations.append("غير موزع - اكتملت السعة")
                
                df_sorted['التخصص النهائي'] = allocations
                
                # ----------------- الإخراج الاحترافي (ملف إكسيل فاخر ومتعدد الأوراق) -----------------
                output = io.BytesIO()
                writer = pd.ExcelWriter(output, engine='xlsxwriter')
                workbook = writer.book
                
                # إعدادات تنسيق الخلايا
                header_format = workbook.add_format({'bold': True, 'text_wrap': True, 'valign': 'center', 'align': 'center', 'fg_color': '#1e3c72', 'font_color': 'white', 'border': 1})
                cell_format = workbook.add_format({'align': 'center', 'valign': 'center', 'border': 1})
                
                # 1. ورقة الإحصائيات الشاملة
                summary_data = df_sorted['التخصص النهائي'].value_counts().reset_index()
                summary_data.columns = ['البيان (التخصص)', 'العدد الفعلي الموزع']
                summary_data.to_excel(writer, sheet_name='إحصائيات التوزيع', index=False)
                worksheet_summary = writer.sheets['إحصائيات التوزيع']
                worksheet_summary.right_to_left()
                worksheet_summary.set_column('A:A', 30, cell_format)
                worksheet_summary.set_column('B:B', 20, cell_format)
                for col_num, value in enumerate(summary_data.columns.values):
                    worksheet_summary.write(0, col_num, value, header_format)
                
                # 2. أوراق العمل المستقلة لكل تخصص
                specialties = df_sorted['التخصص النهائي'].unique()
                for spec in specialties:
                    spec_df = df_sorted[df_sorted['التخصص النهائي'] == spec].copy()
                    
                    # إخفاء الأعمدة غير الضرورية للطباعة وتنسيق التسلسل
                    cols_to_drop = ['التخصص النهائي', 'القسم']
                    spec_df = spec_df.drop(columns=[c for c in cols_to_drop if c in spec_df.columns])
                    spec_df.reset_index(drop=True, inplace=True)
                    spec_df.index += 1 # تسلسل يبدأ من 1
                    spec_df.index.name = 'م'
                    spec_df.reset_index(inplace=True)
                    
                    sheet_name = str(spec)[:31] # الحد الأقصى لاسم الورقة في إكسيل
                    spec_df.to_excel(writer, sheet_name=sheet_name, index=False)
                    worksheet = writer.sheets[sheet_name]
                    worksheet.right_to_left() # اتجاه من اليمين لليسار
                    
                    # ضبط عروض الأعمدة لتناسب الطباعة
                    worksheet.set_column('A:A', 5, cell_format)   # م
                    worksheet.set_column('B:B', 30, cell_format)  # الاسم
                    worksheet.set_column('C:C', 18, cell_format)  # الرقم القومي
                    worksheet.set_column('D:D', 15, cell_format)  # الهاتف
                    worksheet.set_column('E:E', 10, cell_format)  # المجموع
                    worksheet.set_column('F:F', 10, cell_format)  # النسبة
                    worksheet.set_column('G:G', 15, cell_format)  # التقدير
                    worksheet.set_column('H:N', 16, cell_format)  # الرغبات
                    
                    # تلوين ترويسة الجدول
                    for col_num, value in enumerate(spec_df.columns.values):
                        worksheet.write(0, col_num, value, header_format)
                
                writer.close()
                output.seek(0)
                # -----------------------------------------------------------------------------
                
                st.success("✅ تمت عملية الفرز وإنشاء الكشوفات النهائية بنجاح!")
                st.download_button(
                    label="📥 تحميل كشوفات الكنترول النهائية (ملف Excel منسق)",
                    data=output,
                    file_name='Official_Control_Distribution.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                )
            else:
                st.error("⚠️ لا توجد بيانات للطلاب حتى الآن لإجراء التنسيق.")
    st.stop()

# 3. عرض الشعارات الأكاديمية والعنوان الرئيسي
col_logo1, col_title, col_logo2 = st.columns([1, 4, 1])

with col_logo1:
    if os.path.exists("fac_logo.png"):
        st.image("fac_logo.png", use_container_width=True)

with col_title:
    st.markdown("""
        <div class="main-title">
            <h1>قسم الرياضة الجماعية وألعاب المضرب - كلية علوم الرياضة - جامعة المنيا (2026 - 2027)</h1>
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
        <li><b>استدعاء البيانات:</b> ابدأ بكتابة أول حرفين من اسمك في خانة البحث أدناه، وقم باختياره لتظهر درجاتك.</li>
        <li><b>حماية البيانات:</b> يجب إدخال (الرقم القومي) بشكل صحيح. إذا كنت تعدل رغباتك، يجب أن يتطابق مع الرقم الذي سجلت به أول مرة.</li>
        <li><b>ترتيب الرغبات:</b> يجب ترتيب <b>جميع التخصصات السبعة</b> دون تكرار.</li>
        <li><b>مواعيد وقابلية التعديل:</b> ⏳ يفتح باب التسجيل والتعديل من يوم <b>الأحد 9-8-2026</b> حتى يوم <b>السبت 22-8-2026</b>.</li>
        <li><b>التواصل والإيصال:</b> 📱 بعد حفظ رغباتك، انضم لجروب الواتساب الرسمي للدفعة، وقم بطباعة الإيصال كملف PDF باسمك.</li>
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

def get_dept(row):
    for col in ['القسم', 'شعبة', 'التخصص', 'البرنامج']:
        if col in row.index and pd.notna(row[col]):
            return str(row[col])
    return "غير محدد"

# 7. البحث الذكي المنسدل
selected_name = st.selectbox("🔍 ابحث عن اسمك (اكتب أول حرفين من اسمك للبحث):", ["اختر اسم الطالب من هنا..."] + student_names)

if selected_name and selected_name != "اختر اسم الطالب من هنا...":
    student_data = df[df['الاسم'] == selected_name].iloc[0]
    dept_name = get_dept(student_data)
    
    saved_record = None
    if os.path.exists("student_requests.xlsx"):
        df_reqs = pd.read_excel("student_requests.xlsx", dtype=str)
        match = df_reqs[df_reqs['الاسم'] == selected_name]
        if not match.empty:
            saved_record = match.iloc[0]

    st.success(f"✅ أهلاً بك يا {selected_name}.. تم العثور على بياناتك بنجاح!")
    
    colA, colB, colC, colD = st.columns(4)
    with colA:
        st.text_input("المجموع الكلي", value=str(student_data['المجموع']), disabled=True)
    with colB:
        st.text_input("النسبة المئوية (%)", value=str(student_data['النسبة']), disabled=True)
    with colC:
        st.text_input("التقدير الأكاديمي", value=str(student_data['التقدير']), disabled=True)
    with colD:
        st.text_input("القسم / الشعبة", value=dept_name, disabled=True)
        
    st.markdown("---")
    
    st.markdown("### 🔒 الخطوة الأمنية: إدخال الرقم القومي (بمثابة كلمة السر)")
    
    nat_id = st.text_input("الرقم القومي (14 رقماً):", max_chars=14, placeholder="أدخل الرقم القومي الخاص بك للتحقق")
    phone = st.text_input("رقم الهاتف (واتساب):", max_chars=11, placeholder="01xxxxxxxx0")
    
    can_proceed = False
    if len(nat_id) == 14 and len(phone) >= 10:
        if saved_record is not None:
            saved_nat_id = str(saved_record['الرقم القومي']).strip().split('.')[0] 
            current_nat_id = str(nat_id).strip()
            
            if current_nat_id == saved_nat_id:
                st.info("💡 تم التحقق من هويتك بنجاح. يمكنك الآن تعديل رغباتك المسجلة مسبقاً وإعادة الحفظ.")
                can_proceed = True
            else:
                st.error("❌ تحذير أمني: الرقم القومي المدخل لا يتطابق مع الرقم الذي تم التسجيل به مسبقاً لهذا الاسم. لا يمكنك الدخول.")
                can_proceed = False
        else:
            st.success("🔓 تم التحقق الأولي! يمكنك الآن ترتيب رغباتك أدناه (تذكر أن هذا الرقم القومي سيكون كلمة سرك للتعديل لاحقاً):")
            can_proceed = True
    else:
        st.warning("🔒 يرجى إدخال الرقم القومي المكون من 14 رقماً ورقم الهاتف لفتح خانات ترتيب الرغبات.")

    if can_proceed:
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

        r1_opts = ["اختر التخصص..."] + all_options
        r1_val = get_saved_choice(1)
        r1 = st.selectbox("⭐ الرغبة الأولى (الأساسية):", r1_opts, index=get_index(r1_val, all_options))
        
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
                    "الرقم القومي": [str(nat_id)],
                    "رقم الهاتف": [str(phone)],
                    "المجموع": [student_data['المجموع']],
                    "النسبة": [student_data['النسبة']],
                    "التقدير": [student_data['التقدير']],
                    "القسم": [dept_name],
                    "رغبة 1": [r1], "رغبة 2": [r2], "رغبة 3": [r3],
                    "رغبة 4": [r4], "رغبة 5": [r5], "رغبة 6": [r6], "رغبة 7": [r7]
                })
                
                if os.path.exists("student_requests.xlsx"):
                    df_requests = pd.read_excel("student_requests.xlsx", dtype=str)
                    df_requests = df_requests[df_requests['الاسم'] != selected_name]
                    df_requests = pd.concat([df_requests, new_data], ignore_index=True)
                else:
                    df_requests = new_data
                    
                df_requests.to_excel("student_requests.xlsx", index=False)
                
                st.session_state['just_saved'] = True
                st.balloons()
                st.success(f"🎉 مبروك يا {selected_name}! تم حفظ وتأكيد رغباتك السبعة بنجاح.")

        if saved_record is not None or st.session_state.get('just_saved', False):
            cur_r1 = r1 if 'r1' in locals() else saved_record.get('رغبة 1')
            cur_r2 = r2 if 'r2' in locals() else saved_record.get('رغبة 2')
            cur_r3 = r3 if 'r3' in locals() else saved_record.get('رغبة 3')
            cur_r4 = r4 if 'r4' in locals() else saved_record.get('رغبة 4')
            cur_r5 = r5 if 'r5' in locals() else saved_record.get('رغبة 5')
            cur_r6 = r6 if 'r6' in locals() else saved_record.get('رغبة 6')
            cur_r7 = r7 if 'r7' in locals() else saved_record.get('رغبة 7')

            receipt_html = f"""
            <!DOCTYPE html>
            <html lang="ar" dir="rtl">
            <head>
                <meta charset="UTF-8">
                <title>{selected_name}</title>
                <style>
                    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
                    body {{
                        font-family: 'Cairo', sans-serif;
                        background-color: #fcfcfc;
                        margin: 0;
                        padding: 10px;
                        direction: rtl;
                        text-align: right;
                    }}
                    .receipt-box {{
                        background: #ffffff;
                        border: 2px solid #1e3c72;
                        padding: 25px;
                        border-radius: 15px;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                    }}
                    .header {{
                        text-align: center;
                        border-bottom: 2px solid #1e3c72;
                        padding-bottom: 15px;
                        margin-bottom: 15px;
                    }}
                    .header h2 {{
                        color: #1e3c72;
                        margin: 0;
                        font-size: 20px;
                    }}
                    .header p {{
                        color: #555;
                        margin: 5px 0 0 0;
                        font-size: 13px;
                    }}
                    .content p {{
                        font-size: 14px;
                        line-height: 1.8;
                        margin: 6px 0;
                        color: #333;
                    }}
                    ol {{
                        padding-right: 20px;
                        font-weight: bold;
                        margin: 10px 0;
                    }}
                    ol li {{
                        font-size: 14px;
                        margin-bottom: 6px;
                        color: #2c3e50;
                    }}
                    .footer {{
                        text-align: center;
                        margin-top: 20px;
                        font-size: 11px;
                        color: #777;
                        border-top: 1px solid #eee;
                        padding-top: 10px;
                    }}
                    .print-btn-container {{
                        text-align: center;
                        background: #f1f8e9;
                        border: 1px solid #81c784;
                        padding: 15px;
                        border-radius: 10px;
                        margin-top: 20px;
                    }}
                    .print-btn {{
                        background: linear-gradient(135deg, #2e7d32 0%, #43a047 100%);
                        color: white;
                        padding: 12px 25px;
                        font-size: 17px;
                        font-weight: bold;
                        border: none;
                        border-radius: 8px;
                        cursor: pointer;
                        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
                        width: 100%;
                        font-family: 'Cairo', sans-serif;
                    }}
                    .wa-btn {{
                        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
                        color: white;
                        padding: 12px 25px;
                        font-size: 17px;
                        font-weight: bold;
                        border: none;
                        border-radius: 8px;
                        cursor: pointer;
                        box-shadow: 0 4px 10px rgba(37, 211, 102, 0.3);
                        width: 100%;
                        font-family: 'Cairo', sans-serif;
                        margin-bottom: 12px;
                    }}
                    .btn-hover:hover {{
                        opacity: 0.95;
                        transform: translateY(-1px);
                    }}
                    @media print {{
                        .print-btn-container {{
                            display: none;
                        }}
                        .receipt-box {{
                            border: none;
                            box-shadow: none;
                            padding: 0;
                        }}
                    }}
                </style>
            </head>
            <body>
                <div class="receipt-box">
                    <div class="header">
                        <h2>إيصال تسجيل رغبات التخصصات الأكاديمية</h2>
                        <p>قسم الرياضة الجماعية وألعاب المضرب - كلية علوم الرياضة - جامعة المنيا (2026 - 2027)</p>
                    </div>
                    <div class="content">
                        <p><b>اسم الطالب:</b> {selected_name}</p>
                        <p><b>الرقم القومي:</b> {nat_id}</p>
                        <p><b>رقم الواتساب:</b> {phone}</p>
                        <p><b>القسم / الشعبة:</b> {dept_name}</p>
                        <p><b>المجموع الكلي:</b> {student_data['المجموع']} | <b>النسبة المئوية:</b> {student_data['النسبة']}% | <b>التقدير:</b> {student_data['التقدير']}</p>
                        <hr style="border: 0; border-top: 1px dashed #ccc; margin: 15px 0;">
                        <h4 style="color: #1e3c72; margin-bottom: 10px;">ترتيب الرغبات المعتمد:</h4>
                        <ol>
                            <li>الرغبة الأولى: {cur_r1}</li>
                            <li>الرغبة الثانية: {cur_r2}</li>
                            <li>الرغبة الثالثة: {cur_r3}</li>
                            <li>الرغبة الرابعة: {cur_r4}</li>
                            <li>الرغبة الخامسة: {cur_r5}</li>
                            <li>الرغبة السادسة: {cur_r6}</li>
                            <li>الرغبة السابعة: {cur_r7}</li>
                        </ol>
                    </div>
                    <div class="footer">
                        تم استخراج هذا المستند إلكترونياً من منصة الكنترول الرسمية ويعتبر مستنداً رسمياً للتسجيل.
                    </div>
                </div>
                
                <div class="print-btn-container">
                    <a href="https://chat.whatsapp.com/IvBUaPqw5RfExr4ZrEjjWV" target="_blank" style="text-decoration: none;">
                        <button class="wa-btn btn-hover">
                            💬 انضم الآن لجروب الواتساب الرسمي
                        </button>
                    </a>
                    <button class="print-btn btn-hover" onclick="window.print()">
                        🖨️ طباعة أو حفظ الإيصال (PDF)
                    </button>
                    <p style="margin-top: 8px; color: #2e7d32; font-weight: 700; font-size: 14px; margin-bottom: 0;">
                        📌 احفظ رغباتك وانضم للجروب لمتابعة أحدث التعليمات
                    </p>
                </div>
            </body>
            </html>
            """
            components.html(receipt_html, height=650, scrolling=True)
