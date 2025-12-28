# import streamlit as st
# import pandas as pd
# import pdfplumber
# import io
# import json 
# import os
# from dotenv import load_dotenv
# import google.generativeai as genai 
# from pydantic import BaseModel, Field 
# from typing import List, Optional

# # ==========================================
# # 1. CONFIGURATION (LOAD FROM .ENV)
# # ==========================================

# # Load environment variables 
# load_dotenv()

# # Fetch the key securely
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("gemini")

# if not GOOGLE_API_KEY:
#     st.error("Google API Key not found. Please set it in environment variables.")
#     st.stop()

# # ==========================================
# # 2. DATA STRUCTURE
# # ==========================================

# class ContactInfo(BaseModel):
#     name: Optional[str] = Field(None, description="Full Name")
#     email: Optional[str] = Field(None, description="Email Address")
#     phone: Optional[str] = Field(None, description="Phone Number")
#     linkedin: Optional[str] = Field(None, description="LinkedIn URL")

# class Project(BaseModel):
#     title: str = Field(..., description="Project Title")
#     tech_stack: Optional[str] = Field(None, description="Tech used")

# class ResumeData(BaseModel):
#     contact: ContactInfo
#     skills: List[str] = Field(default_factory=list, description="List of all technical skills")
#     projects: List[Project] = Field(default_factory=list, description="ALL projects found in resume")
#     education_degree: Optional[str] = Field(None, description="Latest Degree Name")
#     education_college: Optional[str] = Field(None, description="College Name")
#     years_experience: Optional[str] = Field(None, description="Total years of experience or 'Fresher'")

# # ==========================================
# # 3. CORE LOGIC
# # ==========================================

# def extract_text_from_pdf(file_bytes):
#     """Extracts text from PDF bytes."""
#     text = ""
#     try:
#         with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
#             for page in pdf.pages:
#                 extracted = page.extract_text()
#                 if extracted:
#                     text += extracted + "\n"
#     except Exception as e:
#         st.error(f"Error reading PDF: {e}")
#     return text

# def analyze_resume_with_ai(raw_text: str) -> Optional[ResumeData]:
#     """
#     Sends text to Gemini using the key from .env
#     """
#     # FIX 1: Use the correct variable name GOOGLE_API_KEY (not API_KEY)
#     if not GOOGLE_API_KEY:
#         st.error("❌ API Key Missing!")
#         return None

#     try:
#         genai.configure(api_key=GOOGLE_API_KEY)
#         model = genai.GenerativeModel('gemini-2.5-flash') # Using stable model name

#         prompt = f"""
#         Extract the following details from the resume text below into JSON format:
#         1. Contact Info (Name, Email, Phone, LinkedIn)
#         2. Latest Education (Degree, College)
#         3. All Technical Skills (as a simple list of strings)
#         4. ALL Projects (Title and Tech Stack only). 
#            **CRITICAL INSTRUCTION: Do not limit the number of projects. If the resume has 4 projects, extract 4. If it has 10, extract 10. Extract EVERY project listed.**
#         5. Years of Experience (or "Fresher")

#         RESUME TEXT:
#         {raw_text}
        
#         Return strictly valid JSON matching this schema:
#         {{
#             "contact": {{ "name": "", "email": "", "phone": "", "linkedin": "" }},
#             "education_degree": "",
#             "education_college": "",
#             "skills": ["Python", "SQL", ...],
#             "projects": [
#                 {{ "title": "Project 1", "tech_stack": "Python, Pandas" }},
#                 {{ "title": "Project 2", "tech_stack": "React, Node" }},
#                 ... (Extract ALL projects found)
#             ],
#             "years_experience": ""
#         }}
#         """

#         response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
#         json_data = json.loads(response.text)
#         return ResumeData(**json_data)

#     except Exception as e:
#         st.error(f"AI Error: {e}")
#         return None

# def convert_to_csv(resumes: List[ResumeData]):
#     """
#     Converts the list of Resume objects into a CSV string.
#     """
#     csv_rows = []
#     for r in resumes:
#         # Flatten ALL projects into a single string
#         project_str = " | ".join([f"{p.title} ({p.tech_stack})" for p in r.projects])
        
#         csv_rows.append({
#             "Name": r.contact.name,
#             "Email": r.contact.email,
#             "Phone": r.contact.phone,
#             "LinkedIn": r.contact.linkedin,
#             "Degree": r.education_degree,
#             "College": r.education_college,
#             "Experience": r.years_experience,
#             "Skills": ", ".join(r.skills[:15]),
#             "Total Projects": len(r.projects),
#             "Projects Details": project_str
#         })
    
#     df = pd.DataFrame(csv_rows)
#     return df.to_csv(index=False).encode('utf-8')

# # ==========================================
# # 4. STREAMLIT UI
# # ==========================================

# st.set_page_config(page_title="Resume to CSV", layout="wide")

# st.title("📄 Secure Resume Batch Processor")
# st.markdown("Upload resumes. Extracts **ALL** projects and details.")

# # FIX 2: UNCOMMENT THIS LINE so uploaded_files actually exists!
# uploaded_files = st.file_uploader("Upload PDF Resumes", type=["pdf"], accept_multiple_files=True)

# if uploaded_files and GOOGLE_API_KEY:
#     if st.button(f"Process {len(uploaded_files)} Files"):
        
#         results = []
#         progress_bar = st.progress(0)
        
#         for idx, file in enumerate(uploaded_files):
#             # 1. Read
#             file_bytes = file.read()
#             raw_text = extract_text_from_pdf(file_bytes)
            
#             # 2. Analyze
#             with st.spinner(f"Reading {file.name}..."):
#                 data = analyze_resume_with_ai(raw_text)
#                 if data:
#                     results.append(data)
            
#             progress_bar.progress((idx + 1) / len(uploaded_files))
        
#         if results:
#             st.success("✅ Done! All projects extracted.")
            
#             # Convert to CSV
#             csv_data = convert_to_csv(results)
            
#             # Show Preview
#             df_preview = pd.read_csv(io.BytesIO(csv_data))
#             st.dataframe(df_preview, use_container_width=True)
            
#             # Download Button
#             st.download_button(
#                 label="📥 Download CSV Report",
#                 data=csv_data,
#                 file_name="resume_report.csv",
#                 mime="text/csv"
#             )

# import streamlit as st
# import pandas as pd
# import pdfplumber
# import io
# import json
# import os
# import time
# from dotenv import load_dotenv
# import google.generativeai as genai
# from pydantic import BaseModel, Field
# from typing import List, Optional

# # ==========================================
# # 1. PAGE CONFIG & STYLING (MUST BE FIRST)
# # ==========================================
# st.set_page_config(
#     page_title="AI Resume Analyzer Pro",
#     page_icon="🚀",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS for "Best-in-Class" UI
# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
#     /* Global Styles */
#     .stApp {
#         background-color: #0f1116; /* Dark background */
#         font-family: 'Inter', sans-serif; 
#     }
    
#     /* Hide Default Streamlit Menu */
#     #MainMenu {visibility: hidden;}
#     footer {visibility: hidden;}
#     header {visibility: hidden;}

#     /* Custom Header Card */
#     .header-card {
#         background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
#         padding: 2rem;
#         border-radius: 15px;
#         color: white;
#         text-align: center;
#         margin-bottom: 2rem;
#         box-shadow: 0 4px 6px rgba(0,0,0,0.3);
#     }
#     .header-card h1 {
#         margin: 0;
#         font-size: 2.5rem;
#         font-weight: 800;
#     }
#     .header-card p {
#         margin-top: 10px;
#         font-size: 1.1rem;
#         opacity: 0.9;
#     }

#     /* Metric Cards */
#     div[data-testid="stMetric"] {
#         background-color: #1e2329;
#         padding: 15px;
#         border-radius: 10px;
#         border: 1px solid #2d333b;
#     }
#     div[data-testid="stMetricValue"] {
#         color: #58a6ff !important;
#     }

#     /* Primary Button Styling */
#     div.stButton > button {
#         background: linear-gradient(45deg, #238636, #2ea043);
#         color: white;
#         border: none;
#         padding: 0.75rem 2rem;
#         font-weight: 600;
#         border-radius: 8px;
#         width: 100%;
#         transition: transform 0.2s;
#     }
#     div.stButton > button:hover {
#         transform: scale(1.02);
#         box-shadow: 0 4px 12px rgba(46, 160, 67, 0.4);
#     }

#     /* Success Message */
#     .success-box {
#         padding: 1rem;
#         background-color: #0d1117;
#         border: 1px solid #3fb950;
#         border-radius: 8px;
#         color: #3fb950;
#         text-align: center;
#         margin-top: 1rem;
#     }
# </style>
# """, unsafe_allow_html=True)

# # ==========================================
# # 2. SETUP & SECURITY
# # ==========================================
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("gemini")

# # Sidebar Configuration
# with st.sidebar:
#     st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=50)
#     st.header("⚙️ Configuration")
    
#     # API Key Input (Fallback)
#     if not GOOGLE_API_KEY:
#         st.warning("⚠️ API Key not detected")
#         GOOGLE_API_KEY = st.text_input("Enter Gemini API Key", type="password")
#     else:
#         st.success("✅ API Key Active")
    
#     st.divider()
#     st.markdown("**Model:** `gemini-1.5-flash`")
#     st.markdown("**Mode:** `Batch Processing`")
#     st.caption("Designed by Alok Mahadev Tungal")

# if not GOOGLE_API_KEY:
#     st.stop()

# # ==========================================
# # 3. DATA MODELS
# # ==========================================
# class ContactInfo(BaseModel):
#     name: Optional[str] = Field(None)
#     email: Optional[str] = Field(None)
#     phone: Optional[str] = Field(None)
#     linkedin: Optional[str] = Field(None)

# class Project(BaseModel):
#     title: str
#     tech_stack: Optional[str] = Field(None)

# class ResumeData(BaseModel):
#     contact: ContactInfo
#     skills: List[str] = Field(default_factory=list)
#     projects: List[Project] = Field(default_factory=list)
#     education_degree: Optional[str] = Field(None)
#     years_experience: Optional[str] = Field(None)

# # ==========================================
# # 4. LOGIC FUNCTIONS
# # ==========================================
# def extract_text_from_pdf(file_bytes):
#     try:
#         with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
#             return "\n".join([page.extract_text() or "" for page in pdf.pages])
#     except Exception:
#         return ""

# def analyze_resume(text):
#     genai.configure(api_key=GOOGLE_API_KEY)
#     model = genai.GenerativeModel('gemini-1.5-flash')
    
#     prompt = f"""
#     Analyze this resume text and return a valid JSON object.
#     Extract:
#     1. Contact (Name, Email, Phone, LinkedIn)
#     2. Latest Degree
#     3. Years of Experience (e.g. "2 years" or "Fresher")
#     4. Top 10 Technical Skills (list)
#     5. ALL Projects (Title and Tech Stack) - Extract every single project found.

#     RESUME TEXT:
#     {text[:8000]} 

#     JSON SCHEMA:
#     {{
#         "contact": {{ "name": "...", "email": "...", "phone": "...", "linkedin": "..." }},
#         "education_degree": "...",
#         "years_experience": "...",
#         "skills": ["...", "..."],
#         "projects": [
#             {{ "title": "...", "tech_stack": "..." }}
#         ]
#     }}
#     """
#     try:
#         response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
#         return ResumeData(**json.loads(response.text))
#     except Exception as e:
#         return None

# # ==========================================
# # 5. MAIN UI LAYOUT
# # ==========================================

# # HEADER
# st.markdown("""
# <div class="header-card">
#     <h1>🚀 AI Resume Analyzer Pro</h1>
#     <p>Extract insights and projects from bulk PDFs in seconds</p>
# </div>
# """, unsafe_allow_html=True)

# # UPLOAD SECTION
# uploaded_files = st.file_uploader("📂 Drop PDF Resumes Here", type=["pdf"], accept_multiple_files=True)

# if uploaded_files:
#     st.markdown(f"**Selected:** `{len(uploaded_files)} files` ready for processing.")
    
#     # ACTION BUTTON
#     if st.button("✨ Start AI Analysis", use_container_width=True):
        
#         results = []
#         progress_bar = st.progress(0)
#         status_text = st.empty()
        
#         # PROCESSING LOOP
#         for i, file in enumerate(uploaded_files):
#             status_text.markdown(f"🔄 Processing: **{file.name}**")
            
#             # Read & Analyze
#             text = extract_text_from_pdf(file.read())
#             if text:
#                 data = analyze_resume(text)
#                 if data:
#                     results.append(data)
            
#             # Update Progress
#             progress_bar.progress((i + 1) / len(uploaded_files))
#             time.sleep(0.1) # Smooth animation
            
#         progress_bar.empty()
#         status_text.empty()
        
#         # RESULTS DASHBOARD
#         if results:
#             st.markdown('<div class="success-box">✅ Analysis Complete!</div>', unsafe_allow_html=True)
#             st.divider()
            
#             # 1. METRICS ROW
#             c1, c2, c3 = st.columns(3)
#             c1.metric("Resumes Processed", len(results))
            
#             total_projects = sum(len(r.projects) for r in results)
#             c2.metric("Total Projects Found", total_projects)
            
#             avg_skills = int(sum(len(r.skills) for r in results) / len(results))
#             c3.metric("Avg Skills / Candidate", avg_skills)
            
#             st.divider()
            
#             # 2. DATA TABLE PREPARATION
#             table_data = []
#             for r in results:
#                 # Format projects as a clean list for the table
#                 proj_list = [f"• {p.title} ({p.tech_stack})" for p in r.projects]
#                 proj_str = "\n".join(proj_list)
                
#                 table_data.append({
#                     "Name": r.contact.name,
#                     "Experience": r.years_experience,
#                     "Degree": r.education_degree,
#                     "Skills": ", ".join(r.skills),
#                     "Projects Extracted": proj_str, 
#                     "Email": r.contact.email
#                 })
            
#             df = pd.DataFrame(table_data)
            
#             # 3. INTERACTIVE DATAFRAME
#             st.subheader("📊 Candidate Database")
#             st.dataframe(
#                 df,
#                 column_config={
#                     "Name": st.column_config.TextColumn("Candidate Name", width="medium"),
#                     "Projects Extracted": st.column_config.TextColumn("Projects", width="large"),
#                     "Email": st.column_config.LinkColumn("Email"),
#                 },
#                 use_container_width=True,
#                 height=400
#             )
            
#             # 4. DOWNLOAD CSV
#             csv = df.to_csv(index=False).encode('utf-8')
#             st.download_button(
#                 label="📥 Download Full Report (CSV)",
#                 data=csv,
#                 file_name="AI_Resume_Report.csv",
#                 mime="text/csv",
#                 use_container_width=True
#             )



# import streamlit as st
# import pandas as pd
# import pdfplumber
# import io
# import json
# import os
# import time
# from dotenv import load_dotenv
# import google.generativeai as genai
# from pydantic import BaseModel, Field
# from typing import List, Optional

# # ==========================================
# # 1. ADVANCED PAGE CONFIG
# # ==========================================
# st.set_page_config(
#     page_title="Resume Intelligence AI",
#     page_icon="🧠",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # ==========================================
# # 2. ADVANCED CSS (GLASSMORPHISM THEME)
# # ==========================================
# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700&display=swap');
    
#     /* BACKGROUND & FONT */
#     .stApp {
#         background: radial-gradient(circle at top left, #1e1e2f, #0a0a12);
#         color: #e0e0e0;
#         font-family: 'Outfit', sans-serif;
#     }
    
#     /* HIDE DEFAULT STREAMLIT UI */
#     #MainMenu, footer, header {visibility: hidden;}
#     section[data-testid="stSidebar"] {display: none;}
    
#     /* HERO SECTION (TITLE) */
#     .hero-container {
#         text-align: center;
#         padding: 3rem 1rem;
#         background: rgba(255, 255, 255, 0.03);
#         border: 1px solid rgba(255, 255, 255, 0.05);
#         border-radius: 20px;
#         backdrop-filter: blur(10px);
#         margin-bottom: 2rem;
#         box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
#     }
#     .hero-title {
#         font-size: 3.5rem;
#         font-weight: 700;
#         background: linear-gradient(90deg, #00c6ff, #0072ff);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         margin-bottom: 0.5rem;
#     }
#     .hero-subtitle {
#         font-size: 1.2rem;
#         color: #a0a0b0;
#     }

#     /* UPLOAD ZONE STYLE */
#     .stFileUploader {
#         background: rgba(255, 255, 255, 0.02);
#         border: 1px dashed #4b4b60;
#         border-radius: 15px;
#         padding: 2rem;
#         transition: all 0.3s ease;
#     }
#     .stFileUploader:hover {
#         border-color: #0072ff;
#         background: rgba(0, 114, 255, 0.05);
#     }

#     /* METRIC CARDS */
#     div[data-testid="stMetric"] {
#         background: rgba(255, 255, 255, 0.05);
#         border: 1px solid rgba(255, 255, 255, 0.1);
#         border-radius: 12px;
#         padding: 15px;
#         box-shadow: 0 4px 6px rgba(0,0,0,0.1);
#         transition: transform 0.2s;
#     }
#     div[data-testid="stMetric"]:hover {
#         transform: translateY(-5px);
#         border-color: #00c6ff;
#     }
    
#     /* GLOWING BUTTON */
#     div.stButton > button {
#         background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
#         color: white;
#         font-weight: 600;
#         padding: 0.8rem 2.5rem;
#         border-radius: 30px;
#         border: none;
#         box-shadow: 0 0 15px rgba(0, 114, 255, 0.5);
#         transition: all 0.3s ease;
#         text-transform: uppercase;
#         letter-spacing: 1px;
#     }
#     div.stButton > button:hover {
#         box-shadow: 0 0 25px rgba(0, 114, 255, 0.8);
#         transform: scale(1.05);
#     }

#     /* DATAFRAME STYLING */
#     div[data-testid="stDataFrame"] {
#         background: rgba(255, 255, 255, 0.02);
#         border-radius: 10px;
#         padding: 10px;
#     }
# </style>
# """, unsafe_allow_html=True)

# # ==========================================
# # 3. SETUP & LOGIC
# # ==========================================
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("gemini")

# # Data Models
# class ContactInfo(BaseModel):
#     name: Optional[str] = Field(None)
#     email: Optional[str] = Field(None)
#     phone: Optional[str] = Field(None)
#     linkedin: Optional[str] = Field(None)

# class Project(BaseModel):
#     title: str
#     tech_stack: Optional[str] = Field(None)

# class ResumeData(BaseModel):
#     contact: ContactInfo
#     skills: List[str] = Field(default_factory=list)
#     projects: List[Project] = Field(default_factory=list)
#     education_degree: Optional[str] = Field(None)
#     years_experience: Optional[str] = Field(None)

# def extract_text(file_bytes):
#     try:
#         with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
#             return "\n".join([p.extract_text() or "" for p in pdf.pages])
#     except: return ""

# def analyze_resume(text):
#     if not GOOGLE_API_KEY: return None
#     genai.configure(api_key=GOOGLE_API_KEY)
#     model = genai.GenerativeModel('gemini-1.5-flash')
    
#     prompt = f"""
#     Analyze resume. Return JSON.
#     Extract: Name, Email, Phone, LinkedIn, Latest Degree, Exp (Years), Top Skills, ALL Projects.
    
#     RESUME: {text[:8000]}
    
#     JSON SCHEMA:
#     {{
#         "contact": {{ "name": "...", "email": "...", "phone": "...", "linkedin": "..." }},
#         "education_degree": "...",
#         "years_experience": "...",
#         "skills": ["..."],
#         "projects": [ {{ "title": "...", "tech_stack": "..." }} ]
#     }}
#     """
#     try:
#         res = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
#         return ResumeData(**json.loads(res.text))
#     except: return None

# # ==========================================
# # 4. ADVANCED UI LAYOUT
# # ==========================================

# # --- HERO HEADER ---
# st.markdown("""
# <div class="hero-container">
#     <div class="hero-title">Resume Intelligence AI</div>
#     <div class="hero-subtitle">Upload Resumes • Extract Insights • Export Data</div>
# </div>
# """, unsafe_allow_html=True)

# # --- ERROR CHECK ---
# if not GOOGLE_API_KEY:
#     st.error("🔒 **System Locked:** API Key Missing. Please configure your `.env` file.")
#     st.stop()

# # --- MAIN INTERFACE ---
# col1, col2, col3 = st.columns([1, 2, 1])

# with col2:
#     uploaded_files = st.file_uploader("📂 Drag & Drop PDF Resumes", type=["pdf"], accept_multiple_files=True)

# # Only show the "Start" button if files are uploaded
# if uploaded_files:
#     st.markdown("<br>", unsafe_allow_html=True)
    
#     # Centered Button
#     c1, c2, c3 = st.columns([1, 1, 1])
#     with c2:
#         start_process = st.button("🚀 IGNITE ANALYSIS", use_container_width=True)

#     if start_process:
#         # --- PROCESSING UI ---
#         results = []
#         progress_bar = st.progress(0)
#         status_box = st.empty()
        
#         for i, file in enumerate(uploaded_files):
#             status_box.info(f"⚡ Analyzing: **{file.name}**")
#             text = extract_text(file.read())
#             if text:
#                 data = analyze_resume(text)
#                 if data: results.append(data)
            
#             progress_bar.progress((i + 1) / len(uploaded_files))
#             time.sleep(0.05) # UX Animation
            
#         progress_bar.empty()
#         status_box.empty()
        
#         # --- RESULTS DASHBOARD ---
#         if results:
#             st.markdown("---")
#             st.subheader("📊 Intelligence Report")
            
#             # 1. METRICS ROW
#             m1, m2, m3, m4 = st.columns(4)
#             m1.metric("Candidates", len(results))
#             m2.metric("Total Projects", sum(len(r.projects) for r in results))
#             m3.metric("Avg. Experience", f"{len(results)} Yrs" if len(results) > 0 else "N/A") # Placeholder logic
#             m4.metric("Success Rate", "100%")

#             # 2. TABBED VIEW
#             tab1, tab2 = st.tabs(["📄 Detailed Table", "💾 JSON Data"])
            
#             # Prepare Data
#             rows = []
#             for r in results:
#                 proj_str = " • ".join([f"{p.title} [{p.tech_stack}]" for p in r.projects])
#                 rows.append({
#                     "Name": r.contact.name,
#                     "Experience": r.years_experience,
#                     "Degree": r.education_degree,
#                     "Projects": proj_str,
#                     "Skills": ", ".join(r.skills[:5]) + "...",
#                     "Email": r.contact.email,
#                     "LinkedIn": r.contact.linkedin
#                 })
#             df = pd.DataFrame(rows)

#             with tab1:
#                 st.dataframe(
#                     df,
#                     column_config={
#                         "Name": st.column_config.TextColumn("Candidate", width="medium"),
#                         "Projects": st.column_config.TextColumn("Key Projects", width="large"),
#                         "LinkedIn": st.column_config.LinkColumn("Profile"),
#                     },
#                     use_container_width=True,
#                     height=500
#                 )
            
#             with tab2:
#                 st.json([r.dict() for r in results])

#             # 3. EXPORT AREA
#             st.markdown("<br>", unsafe_allow_html=True)
#             csv = df.to_csv(index=False).encode('utf-8')
            
#             col_d1, col_d2, col_d3 = st.columns([1, 2, 1])
#             with col_d2:
#                 st.download_button(
#                     label="📥 DOWNLOAD INTELLIGENCE REPORT (CSV)",
#                     data=csv,
#                     file_name="Resume_Intelligence_Report.csv",
#                     mime="text/csv",
#                     use_container_width=True
#                 )


import streamlit as st
import pandas as pd
import pdfplumber
import io
import json
import os
import time
from dotenv import load_dotenv
import google.generativeai as genai
from pydantic import BaseModel, Field
from typing import List, Optional

# ==========================================
# 1. ADVANCED PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="Resume Intelligence AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. ADVANCED CSS (IMPROVED GLASSMORPHISM & VISIBILITY)
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    /* BACKGROUND & FONT */
    .stApp {
        /* A smoother, slightly lighter dark gradient for better contrast */
        background: radial-gradient(circle at top left, #2a2a3e, #12121a);
        color: #f0f0f0; /* Brighter main text color */
        font-family: 'Outfit', sans-serif;
    }
    
    /* HIDE DEFAULT STREAMLIT UI */
    #MainMenu, footer, header {visibility: hidden;}
    section[data-testid="stSidebar"] {display: none;}
    
    /* HERO SECTION (TITLE) */
    .hero-container {
        text-align: center;
        padding: 4rem 2rem;
        /* Increased opacity for better text readability */
        background: rgba(30, 30, 46, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        backdrop-filter: blur(15px);
        margin-bottom: 3rem;
        box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.4);
    }
    .hero-title {
        font-size: 4rem;
        font-weight: 800;
        /* Brighter gradient for the title */
        background: linear-gradient(90deg, #40d0ff, #0080ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        letter-spacing: -1px;
    }
    .hero-subtitle {
        font-size: 1.4rem;
        color: #d0d0e0; /* Brighter subtitle text */
        font-weight: 400;
    }

    /* UPLOAD ZONE STYLE */
    .stFileUploader {
        background: rgba(30, 30, 46, 0.6);
        border: 2px dashed #5b5b70;
        border-radius: 20px;
        padding: 3rem;
        transition: all 0.3s ease;
        text-align: center;
    }
    .stFileUploader:hover {
        border-color: #40d0ff;
        background: rgba(64, 208, 255, 0.1);
    }
    /* Improve visibility of the upload text and button */
    .stFileUploader > div > div {
        color: #ffffff;
    }
    .stFileUploader button {
        background: #40d0ff;
        color: #0a0a12;
        border: none;
        font-weight: 600;
    }

    /* METRIC CARDS */
    div[data-testid="stMetric"] {
        background: rgba(30, 30, 46, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-8px);
        border-color: #40d0ff;
        box-shadow: 0 12px 24px rgba(64, 208, 255, 0.3);
    }
    /* Improve metric text visibility */
    div[data-testid="stMetricLabel"] {
        color: #c0c0d0;
        font-weight: 500;
    }
    div[data-testid="stMetricValue"] {
        color: #ffffff;
        font-weight: 700;
    }
    
    /* GLOWING BUTTON */
    div.stButton > button {
        background: linear-gradient(90deg, #40d0ff 0%, #0080ff 100%);
        color: white;
        font-weight: 700;
        padding: 1rem 3rem;
        border-radius: 50px;
        border: none;
        box-shadow: 0 0 20px rgba(0, 128, 255, 0.6);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 1.1rem;
    }
    div.stButton > button:hover {
        box-shadow: 0 0 35px rgba(0, 128, 255, 0.9);
        transform: scale(1.03);
    }
    div.stButton > button:active {
        transform: scale(0.98);
    }

    /* DATAFRAME STYLING */
    div[data-testid="stDataFrame"] {
        background: rgba(30, 30, 46, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 15px;
        backdrop-filter: blur(10px);
    }
    /* Improve table text visibility */
    .stDataFrame {
        color: #f0f0f0;
    }
    .stDataFrame [data-testid="stHeader"] {
        background-color: rgba(255, 255, 255, 0.05);
        color: #ffffff;
        font-weight: 600;
    }
    
    /* STATUS BOX */
    .stAlert {
        background: rgba(30, 30, 46, 0.8);
        color: #ffffff;
        border: 1px solid rgba(64, 208, 255, 0.5);
        backdrop-filter: blur(10px);
        border-radius: 12px;
    }
    
    /* TABS */
    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(30, 30, 46, 0.5);
        padding: 5px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .stTabs [data-baseweb="tab"] {
        color: #c0c0d0;
        border-radius: 8px;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(64, 208, 255, 0.2);
        color: #ffffff;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. SETUP & LOGIC
# ==========================================
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("gemini")

# Data Models
class ContactInfo(BaseModel):
    name: Optional[str] = Field(None)
    email: Optional[str] = Field(None)
    phone: Optional[str] = Field(None)
    linkedin: Optional[str] = Field(None)

class Project(BaseModel):
    title: str
    tech_stack: Optional[str] = Field(None)

class ResumeData(BaseModel):
    contact: ContactInfo
    skills: List[str] = Field(default_factory=list)
    projects: List[Project] = Field(default_factory=list)
    education_degree: Optional[str] = Field(None)
    years_experience: Optional[str] = Field(None)

def extract_text(file_bytes):
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            return "\n".join([p.extract_text() or "" for p in pdf.pages])
    except: return ""

def analyze_resume(text):
    if not GOOGLE_API_KEY: return None
    genai.configure(api_key=GOOGLE_API_KEY)
    # MODIFIED: Using gemini-2.5-flash as requested
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    Analyze resume. Return JSON.
    Extract: Name, Email, Phone, LinkedIn, Latest Degree, Exp (Years), Top Skills, ALL Projects.
    
    RESUME: {text[:8000]}
    
    JSON SCHEMA:
    {{
        "contact": {{ "name": "...", "email": "...", "phone": "...", "linkedin": "..." }},
        "education_degree": "...",
        "years_experience": "...",
        "skills": ["..."],
        "projects": [ {{ "title": "...", "tech_stack": "..." }} ]
    }}
    """
    try:
        res = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        return ResumeData(**json.loads(res.text))
    except: return None

# ==========================================
# 4. ADVANCED UI LAYOUT
# ==========================================

# --- HERO HEADER ---
st.markdown("""
<div class="hero-container">
    <div class="hero-title">Resume Intelligence AI</div>
    <div class="hero-subtitle">Upload Resumes • Extract Insights • Export Data</div>
</div>
""", unsafe_allow_html=True)

# --- ERROR CHECK ---
if not GOOGLE_API_KEY:
    st.error("🔒 **System Locked:** API Key Missing. Please configure your `.env` file.")
    st.stop()

# --- MAIN INTERFACE ---
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    uploaded_files = st.file_uploader("📂 Drag & Drop PDF Resumes", type=["pdf"], accept_multiple_files=True)

# Only show the "Start" button if files are uploaded
if uploaded_files:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Centered Button
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        start_process = st.button("🚀 IGNITE ANALYSIS", use_container_width=True)

    if start_process:
        # --- PROCESSING UI ---
        results = []
        progress_bar = st.progress(0)
        status_box = st.empty()
        
        for i, file in enumerate(uploaded_files):
            status_box.info(f"⚡ Analyzing: **{file.name}**")
            text = extract_text(file.read())
            if text:
                data = analyze_resume(text)
                if data: results.append(data)
            
            progress_bar.progress((i + 1) / len(uploaded_files))
            time.sleep(0.05) # UX Animation
            
        progress_bar.empty()
        status_box.empty()
        
        # --- RESULTS DASHBOARD ---
        if results:
            st.markdown("---")
            st.subheader("📊 Intelligence Report")
            
            # 1. METRICS ROW
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Candidates", len(results))
            m2.metric("Total Projects", sum(len(r.projects) for r in results))
            # Simple logic for average experience, can be improved
            total_exp = 0
            exp_count = 0
            for r in results:
                if r.years_experience and r.years_experience.lower() != "fresher":
                    try:
                        # Extract first number found
                        import re
                        match = re.search(r'\d+', r.years_experience)
                        if match:
                            total_exp += int(match.group())
                            exp_count += 1
                    except: pass
            
            avg_exp_str = f"{round(total_exp / exp_count, 1)} Yrs" if exp_count > 0 else "N/A"
            m3.metric("Avg. Experience", avg_exp_str)
            m4.metric("Success Rate", "100%")

            # 2. TABBED VIEW
            tab1, tab2 = st.tabs(["📄 Detailed Table", "💾 JSON Data"])
            
            # Prepare Data
            rows = []
            for r in results:
                proj_str = " • ".join([f"{p.title} [{p.tech_stack}]" for p in r.projects])
                rows.append({
                    "Name": r.contact.name,
                    "Experience": r.years_experience,
                    "Degree": r.education_degree,
                    "Projects": proj_str,
                    "Skills": ", ".join(r.skills[:5]) + "...",
                    "Email": r.contact.email,
                    "LinkedIn": r.contact.linkedin
                })
            df = pd.DataFrame(rows)

            with tab1:
                st.dataframe(
                    df,
                    column_config={
                        "Name": st.column_config.TextColumn("Candidate", width="medium"),
                        "Projects": st.column_config.TextColumn("Key Projects", width="large"),
                        "LinkedIn": st.column_config.LinkColumn("Profile"),
                        "Email": st.column_config.LinkColumn("Email"),
                    },
                    use_container_width=True,
                    height=500
                )
            
            with tab2:
                st.json([r.dict() for r in results])

            # 3. EXPORT AREA
            st.markdown("<br>", unsafe_allow_html=True)
            csv = df.to_csv(index=False).encode('utf-8')
            
            col_d1, col_d2, col_d3 = st.columns([1, 2, 1])
            with col_d2:
                st.download_button(
                    label="📥 DOWNLOAD INTELLIGENCE REPORT (CSV)",
                    data=csv,
                    file_name="Resume_Intelligence_Report.csv",
                    mime="text/csv",
                    use_container_width=True
                )








