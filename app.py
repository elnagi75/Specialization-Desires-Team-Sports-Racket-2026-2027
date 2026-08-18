import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from datetime import date
import os
import io

# --- محرك المزامنة السحابية مع GitHub ---
def push_to_github(filepath):
    try:
        if "GITHUB_TOKEN" in st.secrets and "GITHUB_REPO" in st.secrets:
            from github import Github
            g = Github(st.secrets["GITHUB_TOKEN"])
            repo = g.get_repo(st.secrets["GITHUB_REPO"])
            
            with open(filepath, 'rb') as f:
                content = f.read()
            
            try:
                # محاولة تحديث الملف إذا كان موجوداً
                file_contents = repo.get_contents(filepath)
                repo.update_file(file_contents.path, f"Auto-sync {filepath} from Streamlit", content, file_contents.sha)
            except:
                # إنشاء الملف إذا لم يكن موجوداً
                repo.create_file(filepath, f"Auto-create {filepath} from Streamlit", content)
    except Exception as e:
        print(f"GitHub Sync Error: {e}") 

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="منصة تسجيل الرغبات - الرياضات الجماعية وألعاب المضرب", layout="centered", page_icon="🎓")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; }
    .main-title { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 25px 20px; border-radius: 15px; text-align: center !important; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 25px; }
    .main-title h1 { font-size: 22px !important; font-weight: 900 !important; color: #ffffff !important; line-height: 1.5; margin: 0 !important; text-align: center !important; }
    .stat-card { background: white; border-radius: 12px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.08); border-bottom: 4px solid #1e3c72; transition: transform 0.3s ease; margin-bottom: 15px; height: 180px; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 10px; box-sizing: border-box; }
    .stat-card:hover { transform: translateY(-5px); }
    .stat-card h2 { margin: 0; font-size: 40px; font-weight: 900; color: #333; line-height: 1.1; }
    .stat-card p { margin: 8px 0 0 0; font-size: 16px; font-weight: 700; color: #666; }
    .stat-icon { font-size: 30px; margin-bottom: 5px; }
    .stMarkdown, p, li, label, .stTextInput, .stSelectbox { direction: RTL !important; text-align: right !important; }
    .instructions-box { background-color: #f8f9fa; border-right: 6px solid #1e3c72; border-radius: 10px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 25px; direction: RTL !important; text-align: right !important; }
    .instructions-box h3 { color: #1e3c72; font-weight: 700; margin-top: 0; text-align: right !important; }
    .instructions-box li { font-size: 15px; color: #333; margin-bottom: 8px; font-weight: 600; text-align: right !important; }
    .stSelectbox label, .stTextInput label { font-size: 17px !important; font-weight: 700 !important; color: #2c3e50 !important; text-align: right !important; }
    .stButton>button { width: 100%; background: linear-gradient(135deg, #8B0000 0%, #B22222 100%) !important; color: white !important; font-size: 19px !important; font-weight: 700 !important; padding: 14px !important; border-radius: 10px !important; border: none !important; box-shadow: 0 4px 12px rgba(139, 0, 0, 0.3) !important; transition: 0.3s; }
    .stButton>button:hover { background: linear-gradient(135deg, #A52A2A 0%, #DC143C 100%) !important; transform: translateY(-2px); box-shadow: 0 6px 15px rgba(139, 0, 0, 0.4) !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. لوحة الكنترول ---
st.sidebar.title("👨‍💻 لوحة الكنترول والإدارة")
admin_pass = st.sidebar.text_input("أدخل كلمة المرور:", type="password")

if admin_pass == "2027":
    st.sidebar.success("تم الدخول بنجاح")
    st.title("📥 لوحة تحكم الكنترول المركزية")
    
    tab1, tab2 = st.tabs(["📥 كشف الرغبات الخام", "⚙️ محرك التنسيق والإخراج الذكي"])
    
    with tab1:
            st.info("هنا يتم تجميع بيانات الطلاب الذين سجلوا رغباتهم، ويمكنك تحميل الكشف الخام.")
            if os.path.exists("student_requests.xlsx"):
                try:
                    df_requests = pd.read_excel("student_requests.xlsx", dtype=str)
                except Exception:
                    df_requests = pd.DataFrame()
                
                if not df_requests.empty:
                    st.dataframe(df_requests)
                    with open("student_requests.xlsx", "rb") as f:
                        st.download_button(label="📥 تحميل كشف الرغبات الخام (Excel)", data=f, file_name='student_requests_raw.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                else:
                    st.warning("الملف فارغ أو قيد التحديث.")
            else:
                st.warning("لم يقم أي طالب بالتسجيل حتى الآن.")
            
    with tab2:
        st.markdown("### 🎯 إعداد السعة الاستيعابية للتخصصات")
        col1, col2, col3, col4 = st.columns(4)
        cap_football = col1.number_input("كرة القدم", min_value=0, value=60)
        cap_handball = col2.number_input("كرة اليد", min_value=0, value=50)
        cap_volleyball = col3.number_input("الكرة الطائرة", min_value=0, value=50)
        cap_basketball = col4.number_input("كرة السلة", min_value=0, value=45)
        col5, col6, col7, col8 = st.columns(4)
        cap_hockey = col5.number_input("الهوكي", min_value=0, value=40)
        cap_tennis = col6.number_input("التنس الأرضي", min_value=0, value=45)
        cap_squash = col7.number_input("اسكواش", min_value=0, value=40)
        
        if st.button("⚙️ إجراء التنسيق واستخراج كشوفات الكنترول"):
            if os.path.exists("student_requests.xlsx"):
                df_req = pd.read_excel("student_requests.xlsx", dtype=str)
                df_req['المجموع'] = pd.to_numeric(df_req['المجموع'], errors='coerce').fillna(0)
                df_sorted = df_req.sort_values(by='المجموع', ascending=False).reset_index(drop=True)
                
                capacities = {'كرة القدم': cap_football, 'كرة اليد': cap_handball, 'الكرة الطائرة': cap_volleyball, 'كرة السلة': cap_basketball, 'الهوكي': cap_hockey, 'التنس الأرضي': cap_tennis, 'اسكواش': cap_squash}
                allocations = []
                current_capacity = {k: 0 for k in capacities.keys()}
                
                for index, row in df_sorted.iterrows():
                    assigned = False
                    for i in range(1, 8):
                        choice = row.get(f'رغبة {i}')
                        if pd.isna(choice): continue
                        if choice in current_capacity and current_capacity[choice] < capacities[choice]:
                            allocations.append(choice)
                            current_capacity[choice] += 1
                            assigned = True
                            break
                    if not assigned: allocations.append("غير موزع - اكتملت السعة")
                
                df_sorted['التخصص النهائي'] = allocations
                
                output = io.BytesIO()
                writer = pd.ExcelWriter(output, engine='xlsxwriter')
                workbook = writer.book
                
                title_format = workbook.add_format({'bold': True, 'font_size': 18, 'valign': 'center', 'align': 'center', 'fg_color': '#f1f8e9', 'font_color': '#2e7d32', 'border': 1})
                header_format = workbook.add_format({'bold': True, 'text_wrap': True, 'valign': 'center', 'align': 'center', 'fg_color': '#1e3c72', 'font_color': 'white', 'border': 1})
                cell_format = workbook.add_format({'align': 'center', 'valign': 'center', 'border': 1})
                highlight_format = workbook.add_format({'bg_color': '#d4edda', 'font_color': '#155724', 'bold': True, 'border': 1, 'align': 'center', 'valign': 'center'})
                
                summary_data = df_sorted['التخصص النهائي'].value_counts().reset_index()
                summary_data.columns = ['البيان (التخصص)', 'العدد الفعلي الموزع']
                summary_data.to_excel(writer, sheet_name='إحصائيات التوزيع', index=False)
                worksheet_summary = writer.sheets['إحصائيات التوزيع']
                worksheet_summary.right_to_left()
                worksheet_summary.set_column('A:A', 30, cell_format)
                worksheet_summary.set_column('B:B', 20, cell_format)
                for col_num, value in enumerate(summary_data.columns.values):
                    worksheet_summary.write(0, col_num, value, header_format)
                
                specialties = df_sorted['التخصص النهائي'].unique()
                for spec in specialties:
                    spec_df = df_sorted[df_sorted['التخصص النهائي'] == spec].copy()
                    cols_to_drop = ['التخصص النهائي', 'القسم']
                    spec_df = spec_df.drop(columns=[c for c in cols_to_drop if c in spec_df.columns])
                    spec_df.reset_index(drop=True, inplace=True)
                    spec_df.index += 1
                    spec_df.index.name = 'م'
                    spec_df.reset_index(inplace=True)
                    
                    sheet_name = str(spec)[:31]
                    spec_df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=1)
                    worksheet = writer.sheets[sheet_name]
                    worksheet.right_to_left() 
                    worksheet.merge_range(0, 0, 0, len(spec_df.columns)-1, f'كشف توزيع الطلاب النهائي - تخصص ( {spec} )', title_format)
                    worksheet.set_row(0, 35)
                    worksheet.set_column('A:A', 5, cell_format)   
                    worksheet.set_column('B:B', 30, cell_format)  
                    worksheet.set_column('C:C', 18, cell_format)  
                    worksheet.set_column('D:D', 15, cell_format)  
                    worksheet.set_column('E:E', 10, cell_format)  
                    worksheet.set_column('F:F', 10, cell_format)  
                    worksheet.set_column('G:G', 15, cell_format)  
                    worksheet.set_column('H:N', 16, cell_format)  
                    for col_num, value in enumerate(spec_df.columns.values): worksheet.write(1, col_num, value, header_format)
                    worksheet.conditional_format(2, 7, len(spec_df)+1, 13, {'type': 'cell', 'criteria': '==', 'value': f'"{spec}"', 'format': highlight_format})
                    worksheet.freeze_panes(2, 0)
                    worksheet.autofilter(1, 0, len(spec_df)+1, len(spec_df.columns)-1)
                
                writer.close()
                output.seek(0)
                st.success("✅ تمت عملية الفرز وإنشاء الكشوفات النهائية بنجاح!")
                st.download_button(label="📥 تحميل كشوفات الكنترول النهائية", data=output, file_name='Official_Control_Distribution.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            else:
                st.error("⚠️ لا توجد بيانات لإجراء التنسيق.")
    st.stop()

# --- 3. قراءة البيانات وحساب الإحصائيات ---
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("data.xlsx")
        return df.dropna(subset=['الاسم'])
    except:
        return None

df = load_data()
total_students = len(df) if df is not None else 0
registered_students = 0

if os.path.exists("student_requests.xlsx"):
    try:
        df_reqs = pd.read_excel("student_requests.xlsx", dtype=str)
        registered_students = len(df_reqs)
    except: pass

remaining_students = max(0, total_students - registered_students)

# --- 4. واجهة المنصة الأساسية ---
col_logo1, col_title, col_logo2 = st.columns([1, 4, 1])
with col_logo1:
    if os.path.exists("fac_logo.png"): st.image("fac_logo.png", use_container_width=True)
with col_title:
    st.markdown("<div class='main-title'><h1>قسم الرياضة الجماعية وألعاب المضرب - كلية علوم الرياضة - جامعة المنيا (2026 - 2027)</h1></div>", unsafe_allow_html=True)
with col_logo2:
    if os.path.exists("uni_logo.png"): st.image("uni_logo.png", use_container_width=True)

col_timer, col_remaining, col_registered = st.columns([2.2, 1, 1])
with col_registered:
    st.markdown(f"<div class='stat-card' style='border-bottom-color: #2e7d32;'><div class='stat-icon'>✅</div><h2 style='color: #2e7d32;'>{registered_students}</h2><p>طالب أتم التسجيل</p></div>", unsafe_allow_html=True)
with col_remaining:
    st.markdown(f"<div class='stat-card' style='border-bottom-color: #d35400;'><div class='stat-icon'>⏳</div><h2 style='color: #d35400;'>{remaining_students}</h2><p>طالب متبقي</p></div>", unsafe_allow_html=True)

with col_timer:
    timer_html = """
    <div dir="rtl" style="background:#fff5f5; padding:12px; border-radius:12px; text-align:center; border-bottom:4px solid #c0392b; height:180px; display:flex; flex-direction:column; justify-content:center;">
        <p style="margin:0 0 10px 0; font-weight:bold; color:#c0392b;">⏰ لغلق المنصة نهائياً</p>
        <div style="display:flex; justify-content:center; gap:10px;">
            <div style="background:white; border:1px solid #ffcccc; border-radius:8px; padding:5px; width:55px;"><div id="d" style="font-size:24px; font-weight:900; color:#c0392b;">0</div><div style="font-size:12px; color:#7f8c8d;">يوم</div></div>
            <div style="font-size:24px; font-weight:900; color:#c0392b;">:</div>
            <div style="background:white; border:1px solid #ffcccc; border-radius:8px; padding:5px; width:55px;"><div id="h" style="font-size:24px; font-weight:900; color:#c0392b;">0</div><div style="font-size:12px; color:#7f8c8d;">ساعة</div></div>
            <div style="font-size:24px; font-weight:900; color:#c0392b;">:</div>
            <div style="background:white; border:1px solid #ffcccc; border-radius:8px; padding:5px; width:55px;"><div id="m" style="font-size:24px; font-weight:900; color:#c0392b;">0</div><div style="font-size:12px; color:#7f8c8d;">دقيقة</div></div>
            <div style="font-size:24px; font-weight:900; color:#c0392b;">:</div>
            <div style="background:white; border:1px solid #ffcccc; border-radius:8px; padding:5px; width:55px;"><div id="s" style="font-size:24px; font-weight:900; color:#c0392b;">0</div><div style="font-size:12px; color:#7f8c8d;">ثانية</div></div>
        </div>
        <div style="margin-top:10px; font-size:13px; color:#7f8c8d;">الموعد النهائي: السبت 22 أغسطس 2026</div>
    </div>
    <script>
    var dest = new Date("Aug 22, 2026 23:59:59").getTime();
    var x = setInterval(function() {
      var now = new Date().getTime(); var dist = dest - now;
      if (dist < 0) { clearInterval(x); return; }
      document.getElementById("d").innerText = Math.floor(dist / (1000 * 60 * 60 * 24));
      document.getElementById("h").innerText = Math.floor((dist % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      document.getElementById("m").innerText = Math.floor((dist % (1000 * 60 * 60)) / (1000 * 60));
      document.getElementById("s").innerText = Math.floor((dist % (1000 * 60)) / 1000);
    }, 1000);
    </script>
    """
    components.html(timer_html, height=195)

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

start_date, end_date, today = date(2026, 8, 8), date(2026, 8, 22), date.today()
if today < start_date: st.warning("⏳ المنصة مغلقة حالياً."); st.stop()
elif today > end_date: st.error("❌ انتهى وقت التسجيل."); st.stop()
if df is None: st.error("⚠️ ملف (data.xlsx) غير موجود."); st.stop()

def get_dept(row):
    for col in ['القسم', 'شعبة', 'التخصص', 'البرنامج']:
        if col in row.index and pd.notna(row[col]): return str(row[col])
    return "غير محدد"

student_names = df['الاسم'].astype(str).tolist()
selected_name = st.selectbox("🔍 ابحث عن اسمك (اكتب أول حرفين من اسمك للبحث):", ["اختر اسم الطالب من هنا..."] + student_names)

saved_record = None
if selected_name != "اختر اسم الطالب من هنا...":
    student_data = df[df['الاسم'] == selected_name].iloc[0]
    dept_name = get_dept(student_data)
    
    if os.path.exists("student_requests.xlsx"):
        df_reqs_search = pd.read_excel("student_requests.xlsx", dtype=str)
        match = df_reqs_search[df_reqs_search['الاسم'] == selected_name]
        if not match.empty: saved_record = match.iloc[0]

    st.success(f"✅ أهلاً بك يا {selected_name}.. تم العثور على بياناتك بنجاح!")
    
    colA, colB, colC, colD = st.columns(4)
    with colA: st.text_input("المجموع الكلي", value=str(student_data['المجموع']), disabled=True)
    with colB: st.text_input("النسبة المئوية (%)", value=str(student_data['النسبة']), disabled=True)
    with colC: st.text_input("التقدير الأكاديمي", value=str(student_data['التقدير']), disabled=True)
    with colD: st.text_input("القسم / الشعبة", value=dept_name, disabled=True)
        
    st.markdown("---")
    st.markdown("### 🔒 الخطوة الأمنية: إدخال الرقم القومي (بمثابة كلمة السر)")
    
    nat_id = st.text_input("الرقم القومي (14 رقماً):", max_chars=14)
    phone = st.text_input("رقم الهاتف (واتساب):", max_chars=11)
    
    can_proceed = False
    if len(nat_id) == 14 and len(phone) >= 10:
        if saved_record is not None:
            if str(nat_id).strip() == str(saved_record['الرقم القومي']).strip().split('.')[0]:
                st.info("💡 تم التحقق من هويتك بنجاح. يمكنك التعديل وإعادة الحفظ.")
                can_proceed = True
            else:
                st.error("❌ تحذير أمني: الرقم القومي المدخل لا يتطابق مع رقم التسجيل السابق.")
        else:
            st.success("🔓 تم التحقق الأولي! رتب رغباتك أدناه:")
            can_proceed = True

    if can_proceed:
        st.markdown("---")
        st.markdown("#### 🎯 حدد رغباتك بترتيب الأولوية:")
        all_opts = ["كرة القدم", "كرة اليد", "الكرة الطائرة", "كرة السلة", "الهوكي", "التنس الأرضي", "اسكواش"]
        
        def g_idx(val, opts): return opts.index(val)+1 if val in opts else 0
        def g_sav(idx): return saved_record.get(f'رغبة {idx}', "اختر التخصص...") if saved_record is not None else "اختر التخصص..."

        r1 = st.selectbox("⭐ الرغبة الأولى:", ["اختر التخصص..."] + all_opts, index=g_idx(g_sav(1), all_opts))
        opts_r1 = [o for o in all_opts if o != r1]
        r2 = st.selectbox("الرغبة الثانية:", ["اختر التخصص..."] + opts_r1, index=g_idx(g_sav(2), opts_r1))
        opts_r2 = [o for o in opts_r1 if o != r2]
        r3 = st.selectbox("الرغبة الثالثة:", ["اختر التخصص..."] + opts_r2, index=g_idx(g_sav(3), opts_r2))
        opts_r3 = [o for o in opts_r2 if o != r3]
        r4 = st.selectbox("الرغبة الرابعة:", ["اختر التخصص..."] + opts_r3, index=g_idx(g_sav(4), opts_r3))
        opts_r4 = [o for o in opts_r3 if o != r4]
        r5 = st.selectbox("الرغبة الخامسة:", ["اختر التخصص..."] + opts_r4, index=g_idx(g_sav(5), opts_r4))
        opts_r5 = [o for o in opts_r4 if o != r5]
        r6 = st.selectbox("الرغبة السادسة:", ["اختر التخصص..."] + opts_r5, index=g_idx(g_sav(6), opts_r5))
        opts_r6 = [o for o in opts_r5 if o != r6]
        r7 = st.selectbox("الرغبة السابعة:", ["اختر التخصص..."] + opts_r6, index=g_idx(g_sav(7), opts_r6))
        
        if st.button("💾 حفظ وتأكيد الرغبات نهائياً"):
            sels = [r1, r2, r3, r4, r5, r6, r7]
            if "اختر التخصص..." in sels: st.error("⚠️ يرجى استكمال جميع الرغبات.")
            elif len(set(sels)) < 7: st.error("⚠️ لا يمكن تكرار نفس التخصص.")
            else:
                new_data = pd.DataFrame({
                    "الاسم": [selected_name], "الرقم القومي": [str(nat_id)], "رقم الهاتف": [str(phone)],
                    "المجموع": [student_data['المجموع']], "النسبة": [student_data['النسبة']],
                    "التقدير": [student_data['التقدير']], "القسم": [dept_name],
                    "رغبة 1": [r1], "رغبة 2": [r2], "رغبة 3": [r3], "رغبة 4": [r4], "رغبة 5": [r5], "رغبة 6": [r6], "رغبة 7": [r7]
                })
                
                if os.path.exists("student_requests.xlsx"):
                    df_save = pd.read_excel("student_requests.xlsx", dtype=str)
                    df_save = df_save[df_save['الاسم'] != selected_name]
                    df_save = pd.concat([df_save, new_data], ignore_index=True)
                else: df_save = new_data
                    
                df_save.to_excel("student_requests.xlsx", index=False)
                
                # --- إرسال الملف لـ GitHub مباشرة ---
                push_to_github("student_requests.xlsx")
                
                st.session_state['just_saved'] = True
                st.rerun()

        if saved_record is not None or st.session_state.get('just_saved', False):
            cr1, cr2, cr3 = r1 if 'r1' in locals() else saved_record.get('رغبة 1'), r2 if 'r2' in locals() else saved_record.get('رغبة 2'), r3 if 'r3' in locals() else saved_record.get('رغبة 3')
            cr4, cr5, cr6, cr7 = r4 if 'r4' in locals() else saved_record.get('رغبة 4'), r5 if 'r5' in locals() else saved_record.get('رغبة 5'), r6 if 'r6' in locals() else saved_record.get('رغبة 6'), r7 if 'r7' in locals() else saved_record.get('رغبة 7')

            receipt = f"""
            <div dir="rtl" style="background:#fff; border:2px solid #1e3c72; padding:20px; border-radius:15px; margin-top:20px;">
                <h3 style="text-align:center; color:#1e3c72;">إيصال تسجيل الرغبات</h3>
                <p><b>الطالب:</b> {selected_name}</p>
                <p><b>الرقم القومي:</b> {nat_id}</p>
                <hr>
                <ol>
                    <li>{cr1}</li><li>{cr2}</li><li>{cr3}</li><li>{cr4}</li><li>{cr5}</li><li>{cr6}</li><li>{cr7}</li>
                </ol>
                <div style="text-align:center; margin-top:15px;">
                    <a href="https://chat.whatsapp.com/IvBUaPqw5RfExr4ZrEjjWV" target="_blank">
                        <button style="background:#25D366; color:white; padding:10px; border:none; border-radius:8px; width:100%; font-weight:bold;">💬 انضم لجروب الواتساب</button>
                    </a>
                </div>
            </div>
            """
            components.html(receipt, height=450)
